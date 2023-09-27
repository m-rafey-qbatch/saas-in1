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
]


