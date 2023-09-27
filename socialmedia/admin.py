from django.contrib import admin
from .models import Post, Reply, UpvoteEvent, UserDebt, Unit

# Register your models here.
class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 1  # Number of empty forms displayed
    fields = ['user', 'content', 'timestamp']  # Fields you want to display in inline replies
    readonly_fields = ['timestamp']  # Making timestamp readonly

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'subject', 'timestamp']  # Fields you want to display in the Post list view
    search_fields = ['subject', 'content', 'user__username']  # Fields by which you want to search
    list_filter = ['timestamp']  # Adding filter by timestamp
    inlines = [ReplyInline]  # Displaying associated replies inline under each post

    # Optionally, if you want to view a post and its replies in detail
    fieldsets = [
        (None, {'fields': ['user', 'subject', 'content', 'timestamp']}),
    ]
    readonly_fields = ['timestamp']

admin.site.register(Post, PostAdmin)

class ReplyAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'content', 'timestamp']
    search_fields = ['content', 'user__username', 'post__subject']
    list_filter = ['timestamp']
    readonly_fields = ['timestamp']

admin.site.register(Reply, ReplyAdmin)



admin.site.register(UpvoteEvent)
admin.site.register(UserDebt)
admin.site.register(Unit)