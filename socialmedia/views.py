from django.shortcuts import render
from .models import Post
from django.contrib.auth.models import User
from users.models import User, PersonalProfile, CompanyProfile, NFT
from django.db.models import Q



def all_posts(request):
    posts = Post.objects.all().order_by('-created_at')

    potential_users_to_follow = User.objects.exclude(
        Q(id=request.user.id) | 
        Q(is_superuser=True) | 
        Q(is_staff=True) |
        Q(personal_profile__full_name='') |
        Q(personal_profile__title='')
    )[:10]


    nft = NFT.objects.filter(user=request.user)
    personal_profile = PersonalProfile.objects.get(user=request.user)
    company_profile = CompanyProfile.objects.get(user=request.user)

    context = {
        'posts': posts,
        'potential_users': potential_users_to_follow,
        'nft': nft,
        'personal_profile': personal_profile,
        'company_profile': company_profile,
    }

    return render(request, 'socialmedia/all_posts.html', context)
