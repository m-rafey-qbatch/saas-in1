from django.contrib import admin
from django.template.defaultfilters import truncatechars
from .models import Post, Reply, UpvoteEvent, UserDebt, Unit, GradeAssignment, Assignment, Submission

# Create a custom admin class for ReplyInline
class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 1  # Number of empty forms displayed
    fields = ['user', 'content', 'timestamp']  # Fields you want to display in inline replies
    readonly_fields = ['timestamp']  # Making timestamp readonly

# Create a custom admin class for Reply
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'content', 'timestamp', 'get_unit']  # Add 'get_unit' to list_display
    search_fields = ['content', 'user__username', 'post__subject']
    list_filter = ['timestamp', 'post__unit']  # Use 'post__unit' in list_filter
    readonly_fields = ['timestamp']

    def get_unit(self, obj):
        return obj.post.unit  # Define a method to get the unit from the related Post
    get_unit.short_description = 'Unit'  # Set a user-friendly column name


# Create a custom admin class for Post
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'subject', 'unit', 'timestamp']  # Add 'unit' to the list_display
    search_fields = ['subject', 'content', 'user__username']
    list_filter = ['timestamp', 'unit']  # Add 'unit' to list_filter
    inlines = [ReplyInline]
    fieldsets = [
        (None, {'fields': ['user', 'subject', 'content', 'unit', 'timestamp']}),
    ]
    readonly_fields = ['timestamp']


class PostInline(admin.TabularInline):
    model = Post
    extra = 0
    fields = ['user', 'subject', 'timestamp']
    readonly_fields = ['timestamp']
    show_change_link = True  # This allows you to jump to the specific Post edit page

class GradeAssignmentInline(admin.TabularInline):
    model = GradeAssignment
    extra = 1
    fields = ['user', 'grade', 'is_completed']

class UnitAdmin(admin.ModelAdmin):
    inlines = [PostInline, GradeAssignmentInline] 

@admin.register(GradeAssignment)
class GradeAssignmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'unit', 'grade', 'is_completed']
    list_filter = ['unit', 'grade']
    search_fields = ['user__username']


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'user', 'timestamp', 'is_on_time', 'status', 'grade', 'resubmitted_count', 'tokens_sent', 'token_tx_hash')
    list_filter = ('status', 'grade', 'assignment')
    search_fields = ('user__username', 'assignment__title')
    readonly_fields = ('timestamp', 'is_on_time', 'token_tx_hash')  # Assuming you don't want the transaction hash to be editable

    def is_on_time(self, obj):
        return obj.is_on_time()
    is_on_time.boolean = True
    is_on_time.short_description = 'Submitted On Time'

    fieldsets = (
        ('Assignment Details', {
            'fields': ('assignment', 'user', 'content')
        }),
        ('Media', {
            'fields': ('image', 'video_upload', 'file_upload')
        }),
        ('Submission Info', {
            'fields': ('timestamp', 'is_on_time', 'status', 'resubmitted_count', 'tokens_sent', 'token_tx_hash')  # Added tokens_sent and token_tx_hash
        }),
        ('Grading', {
            'fields': ('grade', 'admin_feedback')
        }),
    )

    def is_on_time(self, obj):
        return obj.is_on_time()
    is_on_time.boolean = True
    is_on_time.short_description = 'Submitted On Time'



class SubmissionInline(admin.TabularInline):  # or admin.StackedInline for a different layout
    model = Submission
    fields = ('user', 'content', 'image', 'video_upload', 'file_upload', 'timestamp', 'is_accepted')
    readonly_fields = ('timestamp',)
    extra = 0  # No extra forms



class AssignmentAdmin(admin.ModelAdmin):
    inlines = [SubmissionInline]
    list_display = ('id', 'title', 'user', 'unit', 'created_at', 'due_date', 'is_active', 'is_approved')  # 'id' added here
    list_filter = ('is_active', 'is_approved', 'due_date', 'unit')
    search_fields = ('title', 'content', 'user__username', 'unit__name')  # Adjust the unit__name if necessary
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('user', 'unit', 'title', 'content', 'created_at', 'due_date', 'is_active', 'is_approved')
        }),
        ('Media', {
            'fields': ('image', 'video_upload', 'file_upload')
        }),
    )


class UpvoteEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'reply', 'timestamp', 'transaction_hash')
    list_filter = ('timestamp', 'user')
    search_fields = ('user__username', 'reply__content', 'transaction_hash')

    # Optionally, add more customizations here




# Register the custom admin classes for Post and Reply
admin.site.register(Post, PostAdmin)
admin.site.register(Reply, ReplyAdmin)

# Register other models
admin.site.register(UpvoteEvent, UpvoteEventAdmin)
admin.site.register(UserDebt)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Submission, SubmissionAdmin)

