from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
class users(AbstractUser):
    password = models.CharField(max_length=1000,null=True)
    def __str__(self):
        return f"{self.username}:{self.email}"
    

class Projects(models.Model):
    title = models.CharField(max_length=63)
    descp = RichTextField()
    created_by  = models.OneToOneField(users, on_delete=models.CASCADE, related_name="trelloAPIs.Projects.created_by+")
    members = models.ManyToManyField(users, related_name="projects_of_user") #how to make creator a compulsory member
    #can make admin, how to ensure admin as a member/ creator seperate from member
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
    created_by  = models.ForeignKey(users, on_delete=models.CASCADE, related_name="trelloAPIs.Cards.created_by+")
    assigned_to = models.ManyToManyField(users) # cannot be assigned to someone not a memeber of the project
    cards_list = models.ForeignKey(Lists, on_delete=models.CASCADE, related_name="list_cards")

    def __str__(self):
        return f"{self.title}"
    
class Comments(models.Model):
    comment_tym = models.DateTimeField()
    commented_by = models.ForeignKey(users, on_delete=models.CASCADE, related_name="comments_of_user") # prevent comments from getting deleted
    card_comments = models.ForeignKey(Cards, on_delete=models.CASCADE, related_name="comments_in_card")
    comment = RichTextField(default=None)
    def __str__(self):
        return f"{self.comment[:12]} ..."
