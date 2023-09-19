from django.shortcuts import render
from .models import Post, UpvoteEvent, Follow, UserDebt
from django.contrib.auth.models import User
from users.models import PersonalProfile, CompanyProfile, NFT
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .forms import PostForm

from django.shortcuts import get_object_or_404, redirect

from django.db import transaction

from users.views import send_token_to_user

MAX_DEBT_LIMIT = 100



@login_required
def all_posts(request):
    posts = Post.objects.all().order_by('-created_at')
    print("All Posts:", posts)

    followed_user_ids = Follow.objects.filter(follower=request.user).values_list('followed_id', flat=True)

    # Step 2: Update the potential_users_to_follow queryset
    potential_users_to_follow = User.objects.exclude(
        Q(id__in=followed_user_ids) |  # Excluding the users already followed
        Q(id=request.user.id) | 
        Q(is_superuser=True) | 
        Q(is_staff=True) |
        Q(personal_profile__full_name='') |
        Q(personal_profile__title='')
    )[:10]

    nft = NFT.objects.filter(user=request.user)
    personal_profile = PersonalProfile.objects.get(user=request.user)
    company_profile = CompanyProfile.objects.get(user=request.user)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('social')
    else:
        form = PostForm()

    user_paid_posts = request.user.paid_posts.all()
    print("Paid Posts by User:", user_paid_posts)


    context = {
        'posts': posts,
        'potential_users': potential_users_to_follow,
        'nft': nft,
        'personal_profile': personal_profile,
        'company_profile': company_profile,
        'form': form,
        'user_paid_posts': user_paid_posts
    }

    return render(request, 'socialmedia/all_posts.html', context)




@login_required
def upvote_post(request, post_id):
    print(f"Upvote post function called for post_id: {post_id}")
    
    post = get_object_or_404(Post, id=post_id)

    # Check if the post was found
    if post:
        print(f"Found post with ID: {post_id} and content: {post.content}")
    else:
        print(f"Post with ID: {post_id} not found!")
        return redirect('social')

    # Check if the user hasn't already upvoted
    if not post.votes.exists(request.user.id):
        print(f"User {request.user.username} has not yet upvoted post {post_id}")
        
        try:
            # Begin atomic transaction
            with transaction.atomic():
                post.votes.up(request.user.id)
                print(f"Upvoted post {post_id} by user {request.user.username}")

                # Wallet address of the user who created the post
                post_owner_wallet_address = post.user.wallet.wallet_address
                print(f"Post owner's wallet address: {post_owner_wallet_address}")
                
                try:
                    # Send tokens to the post owner
                    tx_hash = send_token_to_user(post_owner_wallet_address)
                    print(f"Token sent to post owner! Transaction hash: {tx_hash}")
                except Exception as e:
                    print(f"Error sending token: {e}")
            
            # Record the upvote event in your database
            upvote_event = UpvoteEvent(user=request.user, post=post, transaction_hash=tx_hash)
            upvote_event.save()
            print(f"Saved upvote event for user {request.user.username} on post {post_id}")

        except Exception as e:
                # Handle the error, for example, log it, send an alert, etc.
                print(f"Error occurred: {e}")

    else:
        print(f"User {request.user.username} has already upvoted post {post_id}")

    return redirect('social')


@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user).order_by('-created_at')
    
    following = user.following.all()
    followers = user.followers.all()

    context = {
        'profile_user': user,  # Renaming this to avoid confusion with the logged-in user
        'posts': posts,
        'following': following,
        'followers': followers,
    }

    return render(request, 'socialmedia/user_profile.html', context)


@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)

    # Check if the user is not trying to follow themselves and 
    # they are not already following the user_to_follow
    if request.user != user_to_follow and not Follow.objects.filter(follower=request.user, followed=user_to_follow).exists():
        Follow.objects.create(follower=request.user, followed=user_to_follow)

        # Reward the user who got followed
        try:
            # Wallet address of the user who was followed
            followed_user_wallet_address = user_to_follow.wallet.wallet_address

            # Send token to the followed user
            tx_hash = send_token_to_user(followed_user_wallet_address, token_amount=1)  # assuming 1 represents $31D token
            print(f"Token sent to {user_to_follow.username} for gaining a follower! Transaction hash: {tx_hash}")
        except Exception as e:
            print(f"Error sending token: {e}")

        return redirect('user_profile', username=username)

    else:
        # Handle cases where users try to follow themselves or already followed users.
        # This can be a message or a redirect to a different page.
        return redirect('user_profile', username=username)



@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, followed=user_to_unfollow).delete()
    return redirect('user_profile', username=username)



@login_required
def pay_to_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user_debt, created = UserDebt.objects.get_or_create(user=request.user)

    # Check if the post is token-gated and if the user has enough "credit"
    if post.is_tokengated_content:
        print(f"Post {post.id} is token-gated")
        if user_debt.amount + post.content_cost <= MAX_DEBT_LIMIT:
            # Increase the user's debt
            user_debt.amount += post.content_cost
            user_debt.save()
            print(f"Updated debt for user {request.user.username}: {user_debt.amount}")
            
            # Add the user to the visible_to field of the post
            post.visible_to.add(request.user)
            post.save()
            print(f"User {request.user.username} added to post {post.id}'s visible_to list")

            # Show the content
            return redirect('social')

        else:
            # Inform the user they have reached their maximum debt limit
            return render(request, 'error.html', {'message': 'You have reached your viewing limit.'})
    else:
        # If the post is not token-gated, just show it
        return redirect('social')



