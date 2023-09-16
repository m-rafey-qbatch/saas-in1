from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField



class PersonalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='personal_profile')
    
    full_name = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=100, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    office = models.CharField(max_length=40, blank=True)
    personal_website = models.URLField(max_length=200, blank=True)
    personal_twitter = models.URLField(max_length=200, blank=True)
    personal_facebook = models.URLField(max_length=200, blank=True)
    personal_linkedin = models.URLField(max_length=200, blank=True)
    personal_instagram = models.URLField(max_length=200, blank=True)
    p_color = models.CharField(max_length=255, default="#f8f9fa")
    p_color_header = models.CharField(max_length=7, default="#000000")

    def __str__(self):
        return self.user.username


class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')
    
    comp = models.CharField(max_length=200, blank=True)
    company_website = models.URLField(max_length=200, blank=True)
    company_logo = models.ImageField(default='default_co.jpg', upload_to='company_logos')
    company_logo_ipfs_uri = models.CharField(max_length=255, null=True, blank=True)
    co_street1 = models.CharField(max_length=200, blank=True)
    co_street2 = models.CharField(max_length=200, blank=True)
    co_city = models.CharField(max_length=200, blank=True)
    co_state = models.CharField(max_length=200, blank=True)
    co_zip = models.CharField(max_length=5, blank=True)
    co_phone = models.CharField(max_length=20, blank=True)
    co_email = models.EmailField(max_length=254, blank=True)
    co_fax = models.CharField(max_length=20, blank=True)
    co_twitter = models.URLField(max_length=200, blank=True)
    co_facebook = models.URLField(max_length=200, blank=True)
    co_linkedin = models.URLField(max_length=200, blank=True)
    co_instagram = models.URLField(max_length=200, blank=True)
    c_color = models.CharField(max_length=7, default="#f8f9fa")
    c_color_header = models.CharField(max_length=7, default="#000000")

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

