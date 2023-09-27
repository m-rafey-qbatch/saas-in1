from django.contrib import admin
from .models import PersonalProfile, NFT, Wallet, WebCamUser, QRScanEvent, UserFaceEncoding


admin.site.register(PersonalProfile)

admin.site.register(NFT)

class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'wallet_address', 'private_key_user')

admin.site.register(Wallet, WalletAdmin)
admin.site.register(WebCamUser)

admin.site.register(QRScanEvent)

class UserFaceEncodingAdmin(admin.ModelAdmin):
    list_display = ('user', 'face_encoding_preview')

    def face_encoding_preview(self, obj):
        return str(obj.face_encoding)[:100]  # Display the first 100 characters of the encoding

admin.site.register(UserFaceEncoding, UserFaceEncodingAdmin)