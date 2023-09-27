import os

from django.shortcuts import render
from .models import Post, UpvoteEvent, UserDebt, Reply, Unit
from django.contrib.auth.models import User
from users.models import PersonalProfile, NFT
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from .forms import PostForm, ReplyForm

from django.shortcuts import get_object_or_404, redirect

from django.db import transaction

from users.views import send_token_to_user, get_wallet_details, get_contract_instance, get_contract_details

from django.http import HttpResponseBadRequest, HttpResponseForbidden

from django.contrib import messages

MAX_DEBT_LIMIT = 100



@login_required
def all_posts(request, unit_name=None):
    # Check if the current user is the superuser 
    is_superuser = request.user.is_superuser

    if unit_name:
        unit = get_object_or_404(Unit, name=unit_name)
        if is_superuser:
            posts = Post.objects.filter(is_active=True, unit=unit).order_by('-created_at')
        else:
            posts = Post.objects.filter(is_active=True, unit=unit, is_approved=True).order_by('-created_at')
    else:
        # Use the new logic to modify the query for posts
        if is_superuser:
            posts = Post.objects.filter(is_active=True).order_by('-created_at')
        else:
            posts = Post.objects.filter(is_active=True, is_approved=True).order_by('-created_at')

    post_replies = {}
    for post in posts:
        if is_superuser:
            replies = Reply.objects.filter(post=post, is_active=True).all()
        else:
            replies = Reply.objects.filter(post=post, is_approved=True, is_active=True).all()
        post_replies[post] = replies


    students = User.objects.filter(is_superuser=False)
    nft = NFT.objects.filter(user=request.user)
    personal_profile = PersonalProfile.objects.get(user=request.user)

    if request.method == "POST":
        # Only allow post creation for superuser 
        if not is_superuser:
            return redirect('social')  # Or whatever appropriate action you want to take
        form = PostForm(request.POST, request.FILES, current_unit_name=unit_name)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('social')
    else:
        form = PostForm(current_unit_name=unit_name)

    user_paid_posts = request.user.paid_posts.all()
    print("Paid Posts by User:", user_paid_posts)
    reply_form = ReplyForm()
    units = Unit.objects.all()

    context = {
        'posts': posts,
        'post_replies': post_replies,
        'reply_form': reply_form,
        'nft': nft,
        'unit': units,
        'students': students,
        'personal_profile': personal_profile,
        'form': form,
        'user_paid_posts': user_paid_posts,
        'is_superuser': is_superuser,  # Add this to context if you want to hide/show the form in the template based on user type
    }

    return render(request, 'socialmedia/all_posts.html', context)




@login_required
def reply_to_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Check if the user is a superuser
    if request.user.is_superuser:
        messages.error(request, "Superusers are not allowed to reply to posts.")
        return redirect('social')

    user_reply = Reply.objects.filter(post=post, user=request.user).first()

    # Regular users will only see approved replies
    replies = Reply.objects.filter(post=post, is_approved=True).all()

    if request.method == "POST":
        form = ReplyForm(request.POST, request.FILES, instance=user_reply)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.save()
            if user_reply:
                messages.success(request, 'Your reply has been updated!')
            else:
                messages.success(request, 'Your reply has been added!')
            return redirect('social')  # or redirect to the specific post
        else:
            messages.error(request, 'There was an error processing your reply. Please try again.')
            print("Form errors:", form.errors)  # Add a print statement to display form errors
    else:
        form = ReplyForm(instance=user_reply)

    # Add print statements to inspect data
    print("User:", request.user)
    print("User Reply:", user_reply)
    for reply in replies:
        print("Reply Content:", reply.content)

    context = {
        'reply_form': form,
        'post': post,
        'replies': replies,
    }

    return render(request, 'socialmedia/reply_form.html', context)





@login_required
def upvote_reply(request, reply_id):
    print(f"Upvote reply function called for reply_id: {reply_id}")
    
    reply = get_object_or_404(Reply, id=reply_id)

    # Check if the reply was found
    if reply:
        print(f"Found reply with ID: {reply_id} and content: {reply.content}")
    else:
        print(f"Reply with ID: {reply_id} not found!")
        return redirect('social')

    # Check if the user hasn't already upvoted the reply
    if not reply.votes.exists(request.user.id):
        print(f"User {request.user.username} has not yet upvoted reply {reply_id}")
        
        try:
            # Begin atomic transaction
            with transaction.atomic():
                reply.votes.up(request.user.id)
                print(f"Upvoted reply {reply_id} by user {request.user.username}")

                # Wallet address of the user who created the reply
                reply_owner_wallet_address = reply.user.wallet.wallet_address
                print(f"Reply owner's wallet address: {reply_owner_wallet_address}")
                
                try:
                    # Send tokens to the reply owner
                    tx_hash = send_token_to_user(reply_owner_wallet_address)
                    print(f"Token sent to reply owner! Transaction hash: {tx_hash}")
                except Exception as e:
                    print(f"Error sending token: {e}")
            
            # Record the upvote event in your database
            upvote_event = UpvoteEvent(user=request.user, reply=reply, transaction_hash=tx_hash)
            upvote_event.save()
            print(f"Saved upvote event for user {request.user.username} on reply {reply_id}")

        except Exception as e:
            # Handle the error, for example, log it, send an alert, etc.
            print(f"Error occurred: {e}")

    else:
        print(f"User {request.user.username} has already upvoted reply {reply_id}")

    return redirect('social')  # Adjust this if you have a specific page to show the reply



@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)

    # Retrieve posts, upvotes, user debts, and replies for the user
    posts = Post.objects.filter(user=user)
    replies = Reply.objects.filter(user=user)
    upvote_events = UpvoteEvent.objects.filter(user=user)
    user_debts = UserDebt.objects.filter(user=user)

    # Retrieve personal profile and NFT details for the user
    personal_profile = PersonalProfile.objects.filter(user=user).first()
    nft = NFT.objects.filter(user=user).first()

    context = {
        'profile_user': user,
        'posts': posts,
        'replies': replies,
        'upvote_events': upvote_events,
        'user_debts': user_debts,
        'personal_profile': personal_profile,
        'nft': nft,
    }

    return render(request, 'socialmedia/user_profile.html', context)



@login_required
def approve_content(request, content_type, content_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to approve content.")

    if content_type == "post":
        content = get_object_or_404(Post, id=content_id)
    elif content_type == "reply":
        content = get_object_or_404(Reply, id=content_id)
    else:
        return HttpResponseBadRequest("Invalid content type.")

    content.is_approved = True
    content.save()
    
    messages.success(request, f'{content_type.capitalize()} has been approved!')

    # Redirect back to a relevant page, for simplicity just redirecting to 'social' here.
    return redirect('social')


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



def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Check if the current user is a superuser
    if request.user.is_superuser:
        post.is_active = False
        post.save()
        messages.success(request, 'Post has been deleted.')
        return redirect('social')
    else:
        # Return a forbidden response if the user is not a superuser
        return HttpResponseForbidden("You don't have permission to delete this post.")


def delete_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)

    # Check if the current user is a superuser
    if request.user.is_superuser:
        reply.is_active = False 
        reply.save()
        messages.success(request, 'Reply has been deleted.')
        return redirect('social')  # you might want to redirect somewhere more specific, like back to the post detail
    else:
        # Return a forbidden response if the user is not a superuser
        return HttpResponseForbidden("You don't have permission to delete this reply.")



@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id) 

    if not request.user.is_superuser:
        return redirect('social') 

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('social') 
    else:
        form = PostForm(instance=post)

    context = {'form': form}
    return render(request, 'socialmedia/edit_post.html', context)


@login_required
def user_replies(request, username):
    # Fetch the user by the username
    user = get_object_or_404(User, username=username)
    
    # Fetch all replies for this user
    replies = Reply.objects.filter(user=user)
    
    context = {
        'replies': replies,
    }

    return render(request, 'socialmedia/user_profile.html', context)



def leaderboard_view(request):

    INFURA_ENDPOINT = os.getenv('INFURA_ENDPOINT')
    CONTRACT_ADDRESS = "0xF62D94eF1C18cB71F5D9C5cb7675c1462AD80F54"
    TOKEN_ABI_PATH = "token_abi.json"

    # Get the contract instance
    contract = get_contract_instance(INFURA_ENDPOINT, CONTRACT_ADDRESS, TOKEN_ABI_PATH)
    
    # Fetch the contract details
    details = get_contract_details(contract)

    # Now you can use the contract symbol in this view
    contract_symbol = details['symbol']

    users = User.objects.exclude(is_superuser=True)

    leaderboard_data = []
    for user in users:
        print(f"Fetching wallet details for user: {user.username}")  # Debug print
        if hasattr(user, 'wallet'):  # Change to hasattr to check attribute
            wallet_details = get_wallet_details(user.wallet.wallet_address)
            token_balance = wallet_details.get('token_balance', 0)
            leaderboard_data.append((user, token_balance))

    leaderboard_data.sort(key=lambda x: x[1], reverse=True)

    print(leaderboard_data)  # Debug print: to see the sorted list

    context = {
        'leaderboard': leaderboard_data,
        'contract_symbol': contract_symbol
    }

    return render(request, 'socialmedia/leaderboard.html', context)
