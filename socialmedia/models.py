from django.db import models
from django.contrib.auth.models import User
from vote.models import VoteModel
from django.conf import settings

from django.utils import timezone

from django.core.exceptions import ValidationError


class Unit(models.Model):
    UNIT_CHOICES = [
        ('unit1', 'Unit 1: Dreams for the Future?'),
        ('unit2', 'Unit 2: Feelings in My Money Matters Group'),
        ('unit3', 'Unit 3: Prioritize Spending'),
        ('unit4', 'Unit 4: Budgeting to Reach My Goals'),
        ('unit5', 'Unit 5: Saving to Reach My Goals'),
        ('unit6', 'Unit 6: Understanding Why I Spend Money'),
        ('unit7', 'Unit 7: Managing My Debt'),
        ('unit8', 'Unit 8: Protecting My Identity'),
        ('unit9', 'Unit 9: Helping Other Teens Reach Their Goals'),
    ]

    name = models.CharField(max_length=200, choices=UNIT_CHOICES)
    
    def __str__(self):
        return self.get_name_display()



class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    subject = models.CharField(max_length=200, null=True)
    content = models.TextField(max_length=2000)

    is_tokengated_content = models.BooleanField(default=False)
    content_cost = models.IntegerField(null=True, blank=True)
    
    visible_to = models.ManyToManyField(User, related_name="paid_posts")

    image = models.ImageField(upload_to='post_images/', null=True, blank=True)  # Add this
    video = models.FileField(upload_to='post_videos/', null=True, blank=True)  # Add this
    files = models.FileField(upload_to='post_files/', null=True, blank=True)  # Add this
    created_at = models.DateTimeField(auto_now_add=True)

    timestamp = models.DateTimeField(auto_now_add=True)


    is_active = models.BooleanField(default=True)

    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.content[:50]
    
    def clean(self):
        # If is_tokengated_content is True but content_cost is None
        if self.is_tokengated_content and self.content_cost is None:
            raise ValidationError({
                'content_cost': ('Content cost is required when content is token-gated.'),
            })
    


class ReplyQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

class ReplyManager(models.Manager):
    def get_queryset(self):
        return ReplyQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()
    

class Reply(VoteModel, models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    content = models.TextField()
    image = models.ImageField(upload_to='replies/images/', blank=True, null=True) 
    video = models.FileField(upload_to='replies/videos/', blank=True, null=True) 
    files = models.FileField(upload_to='replies/files/', blank=True, null=True)
    is_private = models.BooleanField(default=False) 
    timestamp = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    is_approved = models.BooleanField(default=False)


    objects = ReplyManager()
    
    def __str__(self):
        return self.content[:50]

    @property
    def upvote_count(self):
        return self.upvotes.all().count()
    

class UpvoteEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reply = models.ForeignKey(Reply, related_name='upvotes', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_hash = models.CharField(max_length=66, blank=True, null=True)


class UserDebt(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - {self.amount} tokens debt"


