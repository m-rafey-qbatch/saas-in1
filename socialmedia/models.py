import datetime

from django.db import models
from django.contrib.auth.models import User
from vote.models import VoteModel
from django.conf import settings

from django.utils import timezone

from django.core.exceptions import ValidationError





class Unit(models.Model):
    UNIT_CHOICES = [
        ('unit1', 'Unit 1: Introduction to Girl Code and Team Building'),
        ('unit2', 'Unit 2: Self-Expression Through Art'),
        ('unit3', 'Unit 3: Exploring Technology'),
        ('unit4', 'Unit 4: Digital Storytelling'),
        ('unit5', 'Unit 5: Leadership and Public Speaking'),
        ('unit6', 'Unit 6: Cultural Celebrations and Identity'),
        ('unit7', 'Unit 7: Technology and Art Fusion'),
        ('unit8', 'Unit 8: Social Justice and Advocacy'),
        ('unit9', 'Unit 9: Mentorship and Future Goals'),
        ('unit10', 'Unit 10: Showcase and Celebration'),
    ]

    name = models.CharField(max_length=200, choices=UNIT_CHOICES)
    unit_image = models.ImageField(upload_to='unit_images/', null=True, blank=True)
    
    def __str__(self):
        return self.get_name_display()


class GradeAssignment(models.Model):
    GRADE_CHOICES = [
        ('-', '-'),
        ('A+', 'A+'),
        ('A', 'A'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B', 'B'),
        ('B-', 'B-'),
        ('C+', 'C+'),
        ('C', 'C'),
        ('C-', 'C-'),
        ('D+', 'D+'),
        ('D', 'D'),
        ('D-', 'D-'),
        ('F', 'F'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="grade_assignments")
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="grade_assignments")
    grade = models.CharField(max_length=5, choices=GRADE_CHOICES, null=True, blank=True)
    is_completed = models.BooleanField(default=False)  # A checkbox to indicate completion

    class Meta:
        unique_together = ['user', 'unit']  # ensures each user can have only one grade per unit

    def __str__(self):
        return f"{self.user.username} - {self.unit.name} - {self.grade if self.grade else 'Not Graded'}"


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

    allow_replies = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)

    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

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


class Assignment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, related_name='assignments', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='assignments/images/', blank=True, null=True)
    video_upload = models.FileField(upload_to='assignments/videos/', blank=True, null=True)
    file_upload = models.FileField(upload_to='assignments/files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(default=datetime.date.today)
    
    
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']  # Orders by created_at in descending order

    def __str__(self):
        return self.title
    
    def is_submission_open(self):
        return self.is_active and self.due_date >= timezone.now().date()

  
class Submission(models.Model):
    GRADE_CHOICES = [
        ('-', '-'),
        ('A+', 'A+'),
        ('A', 'A'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B', 'B'),
        ('B-', 'B-'),
        ('C+', 'C+'),
        ('C', 'C'),
        ('C-', 'C-'),
        ('D+', 'D+'),
        ('D', 'D'),
        ('D-', 'D-'),
        ('F', 'F'),
    ]

    STATUS_CHOICES = [
        ('pending_review', 'Pending Review'),
        ('needs_action', 'Needs Further Action'),
        ('accepted', 'Accepted'),
        ('revised', 'Submission Revised'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, related_name='submissions', on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='submissions/images/', blank=True, null=True)
    video_upload = models.FileField(upload_to='submissions/videos/', blank=True, null=True)
    file_upload = models.FileField(upload_to='submissions/files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
    admin_feedback = models.TextField("Admin Feedback", blank=True)
    grade = models.CharField(max_length=3, choices=GRADE_CHOICES, default='-', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_review')
    resubmitted_count = models.IntegerField(default=0)

    tokens_sent = models.IntegerField(default=0, verbose_name="Tokens Sent")
    token_tx_hash = models.CharField(max_length=66, blank=True, null=True, verbose_name="Token Transaction Hash")

    def is_on_time(self):
        """Returns True if the submission was made before the assignment's due date."""
        return self.timestamp.date() <= self.assignment.due_date

    def __str__(self):
        # Updated to include on-time status
        on_time_status = "on time" if self.is_on_time() else "late"
        return f"Submission by {self.user.username} for {self.assignment.title} ({on_time_status})"

    class Meta:
        ordering = ['-timestamp']  # Orders submissions by timestamp in descending order

    def save(self, *args, **kwargs):
        # Check if this is a resubmission
        if self._state.adding is False:  # Check if the object already exists (i.e., not a new creation)
            original = Submission.objects.get(pk=self.pk)
            if original.content != self.content or original.image != self.image or original.video_upload != self.video_upload or original.file_upload != self.file_upload:
                # This is a resubmission, so increment the count
                self.resubmitted_count += 1
                self.status = 'revised'
                
        super().save(*args, **kwargs)

    

class UserDebt(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - {self.amount} tokens debt"


