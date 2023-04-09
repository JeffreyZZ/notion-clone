from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from martor.models import MartorField

from django.db.models.signals import post_save
from django.dispatch import receiver
from random import choice
from os.path import join as path_join
from os import listdir
from os.path import isfile
import datetime
from django.utils import timezone
from django.urls import reverse

class MyAccountManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("Users must have an email")
        
        if not first_name:
            raise ValueError("Users must have a first name")
            
        if not last_name:
            raise ValueError("Users must have a last name")

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        # BUG:save user's default profile, which is NOT used by notion but needed to be compatible 
        # with SOF's user. 
        user.profile.email = email
        user.profile.save()

        return user
        
    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user (
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            password = password,
        )

        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user

class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=254, unique=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyAccountManager()

    class Meta:
        db_table = 'quesnotion_users'
        # this is to ignore the existing 'user' table when is False, no database table 
        # creation or deletion operations will be performed for this model. 
        managed = False 

    def __str__(self):
        return f"{self.email}"
    
    def has_perm(self, perm, obj=None):
        return self.is_staff
    
    def has_module_perms(self, app_label):
        return True

class Page(models.Model):
    name = models.CharField(max_length=64)
    parent = models.ForeignKey("Page", related_name='children', null=True, blank=True, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.CharField(max_length=100, null=True, blank=True)
    closed=models.BooleanField(default=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.name}" 

class Page_element(models.Model):
    page = models.ForeignKey("Page", related_name="page_elements", on_delete=models.CASCADE)
    element_type = models.CharField(max_length=85)
    order_on_page = models.FloatField()
    color = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.id}"

class Heading_1(models.Model):
    heading_text = models.CharField(max_length=85, null=True, blank=True)
    page_element = models.ForeignKey("Page_element", related_name="heading_1", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.heading_text}"

class Heading_2(models.Model):
    heading_text = models.CharField(max_length=85, null=True, blank=True)
    page_element = models.ForeignKey("Page_element", related_name="heading_2", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.heading_text}"

class Text(models.Model):
    text = models.CharField(max_length=5000, null=True, blank=True)
    page_element = models.ForeignKey("Page_element", related_name="text", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text}"

class Kanban(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True)
    page_element = models.ForeignKey("Page_element", related_name="kanban", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

class Kanban_Group(models.Model):
    name = models.CharField(max_length=64)
    color = models.CharField(max_length=100)
    kanban = models.ForeignKey("Kanban", related_name="kanban_group", on_delete=models.CASCADE)
    order = models.FloatField()

    def __str__(self):
        return f"{self.name}"

class Kanban_Card(models.Model):
    description = models.CharField(max_length=100, null=True, blank=True)
    kanban_group = models.ForeignKey("Kanban_Group", related_name="kanban_card", on_delete=models.CASCADE)
    order_on_group = models.FloatField()

    def __str__(self):
        return f"{self.description}"

class PageLink(models.Model):
    page = models.ForeignKey("Page", on_delete=models.CASCADE)
    page_element = models.ForeignKey("Page_element", related_name="page_link", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.page}"

class To_do(models.Model):
    description = models.CharField(max_length=500, null=True, blank=True)
    completed = models.BooleanField()
    page_element = models.ForeignKey("Page_element", related_name="to_do", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.description}"

class Table(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    page_element = models.ForeignKey("Page_element", related_name="table", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}"

class Table_row(models.Model):
    order = models.FloatField()
    table = models.ForeignKey("Table", related_name="rows", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}"

class Table_data(models.Model):
    text = models.CharField(max_length=1000, null=True, blank=True)
    number = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    checkbox = models.BooleanField(null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    property_type = models.CharField(max_length=100)
    header = models.BooleanField()
    width = models.IntegerField()
    order = models.FloatField()
    table_row = models.ForeignKey("Table_row", related_name="data", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}"

class Tag(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    table_data = models.ManyToManyField("Table_data", related_name="tags", blank=True)
    table_head = models.ForeignKey("Table_data", related_name="tag_heads", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

# Begin of Profile
# Profile is copied from SOF to keep the user compatible only between NT and SOF.
# It's NOT used by NT at all for now.
def random_img():
    dir_path = 'media/'
    files = [content for content in listdir(
        dir_path) if isfile(path_join(dir_path, content))]
    return path_join(dir_path, choice(files))

JOB_STATUS = [
    ('looking_for_job', 'Actively looking right now'),
    ('open_but_not_looking', 'Open, but not actively looking'),
    ('not_interested_in_jobs', 'Not interested in jobs'),
]

EXPERIENCE_LEVEL = [
    ('Student','Student'),
    ('Junior', 'Junior'),
    ('Mid_Level', 'Mid Level'),
    ('Senior', 'Senior'),
    ('Lead', 'Lead'),
    ('Manager', 'Manager'),
]

JOB_TYPE_CHOICES = [
    ('FULL_TIME', 'Full Time'),
    ('CONTRCT', 'Contract'),
    ('InternShip', 'InternShip'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=30, default='')
    not_to_Display_Full_name = models.CharField(max_length=30, default='')
    email = models.EmailField(max_length=30, default='')
    location = models.CharField(max_length=30, default='')
    title = models.CharField(max_length=30, default='')
    profile_photo = models.ImageField(upload_to='profile_photos', default='media/isle.jpg')
    about_me = models.CharField(max_length=30, default='', blank=True, null=True)
    website_link = models.URLField(blank=True)
    twitter_link = models.URLField(blank=True)
    github_link = models.URLField(blank=True)
    q_edited_counter = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    reputation = models.IntegerField(default=1)
    is_banned = models.BooleanField(default=False)
    post_edit_inactive_for_six_month = models.IntegerField(default=0)
    is_moderator = models.BooleanField(default=False)
    is_high_moderator = models.BooleanField(default=False)
    targeted_tag = models.CharField(max_length=30, default='Commenter')
# BADGES
    review_close_votes = models.BooleanField(default=False)
    favorite_question_S = models.BooleanField(default=False)
    lifeJacket = models.BooleanField(default=False)
    altruist = models.BooleanField(default=False)

# PRIVILEGES
    commenter = models.BooleanField(default=False)

# OTHERS
    logout_on_all_devices = models.BooleanField(default=False)
    send_email_notifications = models.BooleanField(default=False)
    voting_flags = models.IntegerField(default=0)
    helpful_close_votes = models.IntegerField(default=0)

# DEVELOPER STORY
    name = models.CharField(max_length=30, default='')
    prefered_technologies = models.CharField(max_length=30, default='')
    min_expierence_level = models.CharField(max_length=30,choices=EXPERIENCE_LEVEL, default='')
    max_expierence_level = models.CharField(max_length=30,choices=EXPERIENCE_LEVEL, default='')
    job_type = models.CharField(max_length=30, choices=JOB_TYPE_CHOICES)
    job_search_status = models.CharField(max_length=30, choices=JOB_STATUS)
    phone_number = models.CharField(max_length=30, blank=True, null=True)

    create_posts = models.BooleanField(default=True) # Done
    create_wiki_posts = models.BooleanField(default=False) # Done
    remove_new_user_restrictions = models.BooleanField(default=False) # Done
    voteUpPriv = models.BooleanField(default=False) # Done
    flag_posts = models.BooleanField(default=False) # Done
    comment_everywhere_Priv = models.BooleanField(default=False) # Done
    set_bounties = models.BooleanField(default=False) # Done
    edit_community_wiki = models.BooleanField(default=False)
    voteDownPriv = models.BooleanField(default=False) # Done
    view_close_votes_Priv = models.BooleanField(default=False)
    access_review_queues = models.BooleanField(default=False)
    established_user_Priv = models.BooleanField(default=False) # Done
    create_tags = models.BooleanField(default=False) # Done
    edit_questions_answers = models.BooleanField(default=False) # Done
    cast_close_AND_Reopen_votes = models.BooleanField(default=False) # Done
    accessTo_moderatorTools = models.BooleanField(default=False)
    protect_questions = models.BooleanField(default=False) # Done
    trusted_user_Priv = models.BooleanField(default=False)

    helpful_flags_counter = models.IntegerField(default=0, blank=True, null=True)
    posts_edited_counter = models.IntegerField(default=0, blank=True, null=True)
    suggested_Edit_counter = models.IntegerField(default=0, blank=True, null=True)
    editPostTimeOfUser = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    Refiner_Illuminator_TagPostCounter = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f'{self.user}'

    def get_absolute_url(self):
        return reverse('profile:activityPageTabProfile', kwargs={'user_id': self.user_id,'username': self.user.username})

    @property
    def age(self):
        current_datetime = datetime.datetime.now(timezone.utc)
        return (current_datetime - self.time).days
    
    class Meta:
        db_table = 'profile_profile'
        # this is to ignore the existing 'profile_profile' table when is set to False, 
        # no database table creation or deletion operations will be performed for this model. 
        managed = False 

@receiver(post_save, sender=User)  # add this
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)  # add this
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

#End of Profile


class Question(models.Model):
    post_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=5000, default='')
    body = MartorField()
    date = models.DateTimeField(auto_now_add=True)
    active_date = models.DateTimeField(auto_now=True)
    q_reputation = models.IntegerField(default=0)
    q_edited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='q_edited_by', default='', null=True, blank=True)
    q_edited_time = models.DateTimeField(auto_now_add=True)  
    is_bountied = models.BooleanField(default=False)
    bounty_date_announced = models.DateTimeField(auto_now_add=True)
    limit_exced = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    is_protected = models.BooleanField(default=False)
    why_editing_question = models.CharField(max_length=5000, default='')
    is_deleted = models.BooleanField(default=False)
    answeredOnMinusTwo_Downvote = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False)
    closed_at = models.DateTimeField(auto_now_add=True, blank=True)
    is_answer_accepted = models.BooleanField(default=False)
    deleted_time = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ["-date"]

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(
    #             f"{self.title}-{self.id}", max_length=1000, lowercase=True
    #         )

    def __str__(self):
        return f'[USER] - {self.post_owner} = [TITLE] - {self.title} - [Deleted?] - {self.is_deleted} - [Bountied?] - {self.is_bountied}'

    def get_absolute_url(self):
        # 'slug':self.slug})
        return reverse('qa:questionDetailView', kwargs={'pk': self.pk, })

    @property
    def count_answers(self):
        return Answer.objects.filter(questionans=self).exclude(is_deleted=True).count()

    @property
    def calculate_UpVote_DownVote(self):
        get_Upvotes = self.qupvote_set.count()
        get_DownVotes = self.qdownvote_set.count()
        return get_Upvotes - get_DownVotes

    @property
    def calculate_viewers(self):
        return self.viewers.all().count()

    @property
    def count_all_bookmarkers(self):
        return self.bookmarkquestion_set.all().count()

    @property
    def lastEdited_by(self):
        return self.q_edited_by

    @property
    def get_all_tags(self):
        return self.tags.all()

    # @property
    # def count_questions(self):
    #     return Question.objects.all().count()