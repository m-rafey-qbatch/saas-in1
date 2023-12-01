from django.contrib import admin
from .models import PersonalProfile, NFT, Wallet, WebCamUser, QRScanEvent, UserFaceEncoding, ChatRoom, Message, ResumeWorkExp


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


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0  # Don't show extra empty forms
    readonly_fields = ['sender', 'content', 'timestamp']  # Optionally make them read-only
    can_delete = False  # Optionally prevent deletion

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'display_participants', 'created_at']
    search_fields = ['id', 'participants__username']  # Allow search by ID and participants' username
    list_filter = ['created_at']  # Filter by creation date
    inlines = [MessageInline]

    def display_participants(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    display_participants.short_description = 'Participants'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'content', 'timestamp', 'room']
    search_fields = ['content', 'sender__username']
    list_filter = ['timestamp', 'room']
    ordering = ['-timestamp']  # Order by most recent message first


class ResumeWorkExpAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'job_title', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('company_name', 'job_title')



admin.site.register(ResumeWorkExp, ResumeWorkExpAdmin)