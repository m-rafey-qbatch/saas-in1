from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import PersonalProfile, NFT, Wallet, QRScanEvent


@receiver(post_save, sender=User)
def create_personalprofile(sender, instance, created, **kwargs):
    if created:
        PersonalProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_nft(sender, instance, created, **kwargs):
    if created:
        NFT.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_or_update_wallet(sender, instance, created, **kwargs):
    if created:
        # User is newly created, create a new Wallet instance
        Wallet.objects.create(user=instance)
    else:
        # User already exists, get the existing Wallet instance
        wallet = Wallet.objects.get(user=instance)
        # Update the wallet_address and private_key fields
        wallet.wallet_address = instance.wallet.wallet_address
        wallet.private_key_user = instance.wallet.private_key_user
        wallet.save()


@receiver(post_save, sender=User)
def save_personalprofile(sender, instance, **kwargs):
    instance.personal_profile.save()


@receiver(post_save, sender=User)
def save_nft(sender, instance, **kwargs):
    instance.nft.save()


@receiver(post_save, sender=User)
def save_wallet(sender, instance, **kwargs):
    instance.wallet.save()


@receiver(post_save, sender=User)
def create_qr_scan_event(sender, instance, created, **kwargs):
    if created:  # checks if a new User instance was created
        QRScanEvent.objects.create(user=instance)
    

# Disconnect the personal profile signal
@receiver(pre_save, sender=User)
def pre_save_disconnect_p(sender, **kwargs):
    post_save.disconnect(save_personalprofile, sender=sender)

# Reconnect the personal profile signal
@receiver(post_save, sender=User)
def post_save_reconnect_p(sender, **kwargs):
    post_save.connect(save_personalprofile, sender=sender)




