from django.db import models
from django.contrib.auth.models import User

class WebcamSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions_initiated')
    recognized_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='sessions_recognized')
    name = models.CharField(max_length=255)
    start_timestamp = models.DateTimeField(auto_now_add=True)
    end_timestamp = models.DateTimeField(null=True, blank=True)
    recognized = models.BooleanField(default=False)
    face_recognized = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.name}"
