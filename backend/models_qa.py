from django.db import models
from martor.models import MartorField

from django.db.models.signals import post_save
from django.dispatch import receiver
from random import choice
from simple_history.models import HistoricalRecords
from django.urls import reverse

#region Question
ACTIVE_FOR_CHOICES = [
    ('ANSWERED', 'Answered'),
    ('MODIFIED', 'Modified'),
    ('ASKED', 'Asked'),
]

class Question(models.Model):
    title = models.CharField(max_length=5000, default='')
    body = MartorField()
    date = models.DateTimeField(auto_now_add=True)
    active_date = models.DateTimeField(auto_now=True)
    q_reputation = models.IntegerField(default=0)
    q_edited_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='q_edited_by', default='', null=True, blank=True)
    q_edited_time = models.DateTimeField(auto_now_add=True)  
    is_bountied = models.BooleanField(default=False)
    bounty_date_announced = models.DateTimeField(auto_now_add=True)
    limit_exced = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    is_protected = models.BooleanField(default=False)
    why_editing_question = models.CharField(max_length=5000, default='')
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords(related_name='his', table_name='qa_historicalquestion')
    answeredOnMinusTwo_Downvote = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False)
    closed_at = models.DateTimeField(auto_now_add=True, blank=True)
    is_answer_accepted = models.BooleanField(default=False)
    deleted_time = models.DateTimeField(auto_now_add=True, blank=True)
    reversal_monitor = models.BooleanField(default=False)
    lastActiveFor = models.CharField(choices=ACTIVE_FOR_CHOICES, max_length=5000, default='', blank=True)

    # FK needed by notion
    post_owner = models.ForeignKey('User', on_delete=models.CASCADE)
    viewers = models.ManyToManyField('User', related_name='viewed_posts', blank=True)

    class Meta:
        ordering = ["-date"]
        db_table = "qa_question"
        # this is to ignore the existing 'qa_question' table when is set to False, 
        # no database table creation or deletion operations will be performed for this model. 
        managed = False 

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
#endregion

#region Answer

DELETE_HISTORY = [
    ('DELETED','Deleted'),
    ('UNDELETED','UnDeleted'),
]

class Answer(models.Model):
    a_edited_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='a_edited_time')
    a_edited_time = models.DateTimeField(auto_now=True)
    answer_owner = models.ForeignKey('User', on_delete=models.CASCADE)
    questionans = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    date = models.DateTimeField(auto_now_add=True)
    deletedHistory = models.CharField(max_length=5000, choices=DELETE_HISTORY, default='')
    body = MartorField()
    a_vote_ups = models.ManyToManyField('User', related_name='a_vote_up', blank=True)
    a_vote_downs = models.ManyToManyField('User', related_name='a_vote_down', blank=True)
    accepted = models.BooleanField(default=False)
    a_reputation = models.IntegerField(default=0)
    is_bountied_awarded = models.BooleanField(default=False)
    active_time = models.DateTimeField(auto_now=True)

    why_editing = models.CharField(max_length=5000, default='')
    history = HistoricalRecords(related_name='anshis', table_name='qa_historicalanswer')
    monitor_it = models.BooleanField(default=False)
    why_editing_answer = models.CharField(max_length=5000, default='', blank=True, null=True)

    revival_stage_one = models.BooleanField(default=False, blank=True, null=True)
    necromancer_check = models.BooleanField(default=False, blank=True, null=True)
    is_wiki_answer = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    deleted_time = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        db_table = "qa_answer"
        # this is to ignore the existing 'qa_answer' table when is set to False, 
        # no database table creation or deletion operations will be performed for this model. 
        managed = False 

    def __str__(self):
        return f'[USER] - {self.answer_owner} = [TITLEs] - {self.body}'
    
#endregion

#region Notification
TYPE_OF_NOTI = [
	('comment_answer','comment_answer'),
	('question_comment','question_comment'),
	('community_message','community_message'),
	('question_edit', 'question_edit'),
	('question_reopen_voted','Question ReOpen Voted'),
	('question_suggested_edit', 'Question Suggested Edit'),
	('NEW_ANSWER', 'New_Answer'),
]

class Notification(models.Model):
    noti_receiver = models.ForeignKey('User', on_delete=models.CASCADE, default='', related_name='noti_receiver')
    type_of_noti = models.CharField(max_length=30, choices=TYPE_OF_NOTI, default='')
    url = models.URLField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    question_noti = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='notifications', blank=True, null=True)
    answer_noti = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        db_table = "notification_notification"
        # this is to ignore the existing 'notification_notification' table when is set to False, 
        # no database table creation or deletion operations will be performed for this model. 
        managed = False

    def __str__(self):
        return f"{self.type_of_noti} - [USER] {self.noti_receiver} - [READED?] - {self.is_read}"
#endregion

#region PrivRepNotification
PRIV_NOTIFY_CHOICES = [
	('EDIT_GOT_APPROVED', 'Edit Approved'),
	# ('DOWN_VOTE_ANSWER_REP_M', 'Answer Down Vote Rep Minus'),
	('ANSWER_ACCEPT_REP_P', 'Answer Accept Rep Plus'),
	('BOUNTY_AWARDED_REP_P', 'Bounty Award Rep Plus'),
	('MY_ANSWER_UPVOTE_REP_P', 'Answered Answer Upvote Rep Plus'),
	('QUESTION_DOWNVOTE', 'Question DownVote'),
	('MY_QUESTION_UPVOTE_REP_P', 'Asked Question Upvote Rep Plus'),
	('Privilege_Earned', 'Privilege Earned'),
	('BADGE_EARNED', 'Badge Earned')
]

class PrivRepNotification(models.Model):
    for_user = models.ForeignKey('User', on_delete=models.CASCADE)
    url = models.URLField(null=True, blank=True, default="#")
    for_if = models.CharField(max_length=30,default='')
    date_created_PrivNotify = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    type_of_PrivNotify = models.CharField(max_length=30, choices=PRIV_NOTIFY_CHOICES,default='')
    missingReputation = models.IntegerField(default=0, blank=True, null=True)
    privilegeURL = models.URLField(null=True, blank=True)
    description = models.CharField(max_length=1000, default='')
    question_priv_noti = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)
    answer_priv_noti = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = "notification_privrepnotification"
        # this is to ignore the existing 'notification_prirepnotification' table when is set to False, 
        # no database table creation or deletion operations will be performed for this model. 
        managed = False

    def __str__(self):
        return self.type_of_PrivNotify
#endregion