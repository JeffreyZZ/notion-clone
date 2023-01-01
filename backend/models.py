from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

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
    