from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.fields import related
# Create your models here.
class users(AbstractUser):
    password = models.CharField(max_length=1000,null=True)
    def __str__(self):
        return f"{self.username}:{self.email}"
    

class Projects(models.Model):
    title = models.CharField(max_length=63)
    descp = RichTextField()
    created_by  = models.ForeignKey(users, on_delete=models.CASCADE, related_name="created_projects")
    members = models.ManyToManyField(users, related_name="projects_of_user")
    admins = models.ManyToManyField(users, related_name="projects_of_user_as_admin") 
    def __str__(self):
        return f"{self.title}"
    
    

class Lists(models.Model):
    title = models.CharField(max_length=63)
    lists_project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name="project_lists", null=True)

    def __str__(self):
        return f"{self.title}"

class Cards(models.Model):
    title = models.CharField(max_length=63)
    descp = RichTextField()
    due_date = models.DateTimeField()
    created_by  = models.ForeignKey(users, on_delete=models.CASCADE, related_name="created_cards")
    assigned_to = models.ManyToManyField(users, related_name="assigned_cards") # cannot be assigned to someone not a memeber of the project
    cards_list = models.ForeignKey(Lists, on_delete=models.CASCADE, related_name="list_cards")

    def __str__(self):
        return f"{self.title}"
    
class Comments(models.Model):
    comment_tym = models.DateTimeField(auto_now=True)
    commented_by = models.ForeignKey(users, on_delete=models.CASCADE, related_name="comments_of_user") # prevent comments from getting deleted
    card_comments = models.ForeignKey(Cards, on_delete=models.CASCADE, related_name="comments_in_card")
    comment = RichTextField(default=None)
    def __str__(self):
        return f"{self.comment[:12]} ..."

# models folder, independent models as files: init.py: same for serializer, same for views
# pagination ?