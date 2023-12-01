from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_posts, name='social'),
    path('posts/<str:unit_name>/', views.all_posts, name='all_posts_by_unit'),
    path('upvote/<int:reply_id>/', views.upvote_reply, name='upvote_reply'),
    path('profile/@<str:username>/', views.user_profile, name='user_profile'),
    path('pay_to_view/<int:post_id>/', views.pay_to_view, name='pay_to_view'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('delete_reply/<int:reply_id>/', views.delete_reply, name='delete_reply'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('reply/<int:post_id>/', views.reply_to_post, name='reply_to_post'),
    path('user/<str:username>/replies/', views.user_replies, name='user_replies'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('approve/<str:content_type>/<int:content_id>/', views.approve_content, name='approve_content'),
    path('assign_grade/', views.assign_grade, name='assign_grade'),
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('submissions/update/<int:submission_id>/', views.update_submission_status, name='update_submission_status'),
    path('assignments/<str:unit_name>/', views.all_assignments, name='all_assignments_by_unit'),
    path('assignments/create/', views.assignment_create, name='assignment_create'),
    path('assignments/<int:pk>/edit/', views.assignment_edit, name='assignment_edit'),
    path('assignments/<int:pk>/delete/', views.assignment_delete, name='assignment_delete'),
    path('submit_assignment/<int:assignment_id>/', views.submit_to_assignment, name='submit_to_assignment'),
    path('submissions/<int:submission_id>/', views.submission_detail, name='submission_detail'),
    path('submissions/resubmit/<int:submission_id>/', views.resubmit_submission, name='resubmit_submission'),
]


