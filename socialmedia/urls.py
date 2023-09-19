from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_posts, name='social'),
    path('upvote/<int:post_id>/', views.upvote_post, name='upvote_post'),
    path('profile/@<str:username>/', views.user_profile, name='user_profile'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow_user'),
    path('pay_to_view/<int:post_id>/', views.pay_to_view, name='pay_to_view'),
]

