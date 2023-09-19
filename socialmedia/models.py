from django.db import models
from django.contrib.auth.models import User
from vote.models import VoteModel

class Post(VoteModel, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    subject = models.CharField(max_length=200, null=True)
    content = models.TextField(max_length=280)

    is_tokengated_content = models.BooleanField(default=False)
    content_cost = models.PositiveIntegerField(default=0)
    visible_to = models.ManyToManyField(User, related_name="paid_posts")

    image = models.ImageField(upload_to='post_images/', null=True, blank=True)  # Add this
    video = models.FileField(upload_to='post_videos/', null=True, blank=True)  # Add this
    upvotes = models.PositiveIntegerField(default=0)  # Add this
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]



class UpvoteEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_hash = models.CharField(max_length=66, blank=True, null=True)


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower} follows {self.followed}"
    

class UserDebt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - {self.amount} tokens debt"

