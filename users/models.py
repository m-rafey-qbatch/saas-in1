from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

GRADES = [
    ('', 'Choose...'),
    ('1st Grade', '1st Grade'),
    ('2nd Grade', '2nd Grade'),
    ('3rd Grade', '3rd Grade'),
    ('4th Grade', '4th Grade'),
    ('5th Grade', '5th Grade'),
    ('6th Grade', '6th Grade'),
    ('7th Grade', '7th Grade'),
    ('8th Grade', '8th Grade'),
    ('9th Grade', '9th Grade'),
    ('10th Grade', '10th Grade'),
    ('11th Grade', '11th Grade'),
    ('12th Grade', '12th Grade'),
    ('Freshman - Univeristy', 'Freshman - Univeristy'),
    ('Sophmore - Univeristy', 'Sophmore - Univeristy'),
    ('Junior - Univeristy', 'Junior - Univeristy'),
    ('Senior - Univeristy', 'Senior - Univeristy'),
    ('Adult Learner', 'Adult Learner'),
    ]

CAMPUS = [
    ('', 'Choose...'),
    ('Flint, MI', 'Flint, MI'),
    ('Chicago, IL', 'Chicago, IL'),
    ]




class PersonalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='personal_profile')
    
    full_name = models.CharField(max_length=200, blank=True)
    sbev_campus = models.CharField(max_length=50, blank=True, choices=CAMPUS)
    grade_level = models.CharField(max_length=50, blank=True, choices=GRADES)
    school = models.CharField(max_length=200, blank=True) # Added this
    hometown = models.CharField(max_length=200, blank=True) # Added this
    mobile = models.CharField(max_length=20, blank=True)
    personal_website = models.URLField(max_length=200, blank=True)
    personal_linkedin = models.URLField(max_length=200, blank=True)
    p_color = models.CharField(max_length=255, default="#f8f9fa")
    p_color_header = models.CharField(max_length=7, default="#000000")

    def __str__(self):
        return self.user.username



class NFT(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='nft')

    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(default='default_nft.jpg', upload_to='nft_images/')
    image_ipfs_uri = models.CharField(max_length=255, default='')  
    contract_address = models.CharField(max_length=42, default='')
    token_id = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.user.username


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')

    wallet_address = models.CharField(max_length=100, default='')
    private_key_user = models.CharField(max_length=100, default='')

    def __str__(self):
        return f"Wallet for {self.user.username}"
    
    def save(self, *args, **kwargs):
        # Add any additional logic here if needed

        # Call the default save method to save the object
        super().save(*args, **kwargs)


class WebCamUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='webcamuser')

    webcam_image = models.ImageField(upload_to='webcam_images/')
    verified = models.BooleanField(default=False) 
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" Webcam Photo and Verification for user {self.user.username}"


class QRCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='qrcodes')
    qrcode = models.ImageField(upload_to='qrcodes/')

    def __str__(self):
        return f"QR code for user {self.user.username}"


class QRScanEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    scan_timestamp = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # New field to store IP address
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    tx_hash = models.CharField(max_length=66, blank=True, null=True)

    def __str__(self):
        return f"QR code scan for {self.user.username} at {self.scan_timestamp}"


class UserFaceEncoding(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    face_encoding = models.BinaryField()

    def __str__(self):
        return self.user.username  # This will display the associated user's username in the Django admin.


class ChatRoom(models.Model):
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    chat_id = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        participants = ", ".join([user.username for user in self.participants.all()])
        return f"Chat with {participants}"


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(User, related_name='read_messages', blank=True)

    def __str__(self):
        return f"Message from {self.sender}: {self.content[:50]}"
    


class ResumeWorkExp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    company_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False, verbose_name="Current Job")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Work Experience"
        verbose_name_plural = "Work Experiences"
        ordering = ['-start_date', '-end_date']

    def __str__(self):
        return f"{self.company_name} - {self.job_title}"