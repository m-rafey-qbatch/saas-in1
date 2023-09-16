from django.contrib import admin
from .models import PersonalProfile, CompanyProfile, NFT, Wallet, WebCamUser, QRScanEvent


admin.site.register(PersonalProfile)

admin.site.register(CompanyProfile)

admin.site.register(NFT)

class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'wallet_address', 'private_key_user')

admin.site.register(Wallet, WalletAdmin)

admin.site.register(WebCamUser)

admin.site.register(QRScanEvent)