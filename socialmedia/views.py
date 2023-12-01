import os

from .models import Post, UpvoteEvent, UserDebt, Reply, Unit, Assignment, Submission
from django.contrib.auth.models import User
from users.models import PersonalProfile, NFT
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect


from .forms import PostForm, ReplyForm, AssignmentForm, SubmissionForm

from django.shortcuts import get_object_or_404, redirect, render

from django.db import transaction
from django.db.models import Prefetch

from users.views import send_token_to_user, get_wallet_details, get_contract_instance, get_contract_details

from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect

from django.contrib import messages

from collections import defaultdict

from django.db.models import Q

from .forms import GradeAssignmentForm, SubmissionForm, AssignmentForm
from .models import GradeAssignment

from django.urls import reverse

from django.core.exceptions import PermissionDenied

from django.utils import timezone

from django.db.models import Exists, OuterRef

import json

from dotenv import load_dotenv

from thirdweb import ThirdwebSDK
from thirdweb.types import SDKOptions, GasSettings, GasSpeed
from eth_account import Account
from thirdweb.types.nft import NFTMetadataInput
from thirdweb.types import SDKOptions

from web3 import Web3

from .views import send_token_to_user


MAX_DEBT_LIMIT = 100



@login_required
def all_posts(request, unit_name=None):
    print("Request user:", request.user)

    is_superuser = request.user.is_superuser
    # Initialize forms; AssignmentForm is only for superuser
    form = PostForm(current_unit_name=unit_name)
    assignment_form = AssignmentForm() if is_superuser else None
    submission_form = SubmissionForm()
    reply_form = ReplyForm()

    # Filter posts and assignments based on unit and user type
    unit = None
    if unit_name and unit_name.lower() != 'all':
        unit = get_object_or_404(Unit, name=unit_name)
        posts = Post.objects.filter(unit=unit)
        assignments = Assignment.objects.filter(unit=unit) if is_superuser else Assignment.objects.filter(unit=unit, is_active=True, is_approved=True)
    else:
        posts = Post.objects.all()
        assignments = Assignment.objects.all() if is_superuser else Assignment.objects.filter(is_active=True, is_approved=True)

    
    unapproved_assignments = Assignment.objects.filter(is_approved=False)

    # Construct replies for each post
    post_replies = {post: Reply.objects.filter(post=post) for post in posts}

    if request.method == "POST":
        print("Received POST request")  # To confirm you're receiving a POST request
        if 'create_post' in request.POST:
            print("'create_post' in request.POST")  # To confirm that the condition is met
            
            # Extracting unit_name from the form submission
            unit_id = request.POST.get('unit')

            print(f"Unit name from form: {unit_name}")
            
            if is_superuser:
                print("User is superuser")  # To confirm that the user is a superuser
                form = PostForm(request.POST, request.FILES, current_unit_name=unit_name)
                if form.is_valid():
                    print("Form is valid, creating post...")  # To confirm form validation
                    post = form.save(commit=False)
                    post.user = request.user

                    try:
                        unit_instance = Unit.objects.get(pk=unit_id)
                        post.unit = unit_instance
                    except Unit.DoesNotExist:
                        print(f"No unit found with the ID {unit_id}")
                        # Handle the case where the unit doesn't exist, e.g., by setting to None or using a default
                        post.unit = None  # or a default unit instance

                    
                    post.save()
                    print(f"Post saved with ID {post.pk}")  # To confirm post is saved
                    
                    return redirect('all_posts_by_unit', unit_name=unit_instance.name) if unit_instance else redirect('social')
                else:
                    print(f"Form errors: {form.errors}")  # To print form errors if any
            else:
                print("User is not superuser")

        elif 'create_assignment' in request.POST and is_superuser:
            unit_id = request.POST.get('unit')
            assignment_form = AssignmentForm(request.POST, request.FILES)

            if assignment_form.is_valid():
                assignment = assignment_form.save(commit=False)
                assignment.user = request.user

                try:
                    unit_instance = Unit.objects.get(pk=unit_id)
                    assignment.unit = unit_instance
                except Unit.DoesNotExist:
                    print(f"No unit found with the ID {unit_id}")
                    assignment.unit = None  # or a default unit instance

                assignment.save()

                # Use get_name_display() to get the full name of the unit
                unit_full_name = unit_instance.get_name_display() if unit_instance else "Unknown Unit"
                messages.success(request, f"Assignment for {unit_full_name} has been successfully posted.")
                

                return redirect('all_posts_by_unit', unit_name=unit_instance.name) if unit_instance else redirect('social')

        elif 'submit_assignment' in request.POST and not is_superuser:
            submission_form = SubmissionForm(request.POST, request.FILES)
            if submission_form.is_valid():
                submission = submission_form.save(commit=False)
                submission.user = request.user
                submission.assignment = get_object_or_404(Assignment, id=request.POST.get('assignment_id'))
                submission.save()
                return redirect('assignment_submissions', pk=submission.assignment.pk)

    # Gather additional information for context
    students = User.objects.filter(is_superuser=False)
    nft = NFT.objects.filter(user=request.user)
    personal_profile = PersonalProfile.objects.get(user=request.user)
    user_paid_posts = request.user.paid_posts.all()
    units = Unit.objects.all()
    upvotes_by_user = UpvoteEvent.objects.filter(user=request.user)
    upvoted_reply_ids = upvotes_by_user.values_list('reply_id', flat=True)
    upvoted_replies_by_user = set(upvoted_reply_ids)

    alert_displayed = request.session.get('alert_displayed', False)
    context = {
        'posts': posts,
        'post_replies': post_replies,
        'reply_form': reply_form,
        'nft': nft,
        'unit': unit,
        'units': Unit.objects.all(),
        'current_unit': unit,  # 'unit' now represents the current unit
        'students': students,
        'personal_profile': personal_profile,
        'form': form,
        'upvoted_replies_by_user': upvoted_replies_by_user,
        'user_paid_posts': user_paid_posts,
        'is_superuser': is_superuser,
        'assignments': assignments,
        'assignment_form': assignment_form,
        'submission_form': submission_form,
        'unapproved_assignments': unapproved_assignments,
        'current_date': timezone.now().date(),
        'hide_alert': alert_displayed,  # Changed to set hide_alert directly based on session value
    }

    if not alert_displayed:
        request.session['alert_displayed'] = True

    return render(request, 'socialmedia/all_posts.html', context)





@login_required
def reply_to_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user_reply = None

    # Check if the user is a superuser
    if request.user.is_superuser:
        messages.error(request, "Students are not allowed to reply to posts.")
        return redirect('social')
    
    # Check if the post allows replies
    if not post.allow_replies:
        messages.error(request, "Replies to this post are not allowed.")
        return redirect('social')

    user_reply = Reply.objects.filter(post=post, user=request.user).first()

    if request.user.is_superuser:
        replies = Reply.objects.filter(post=post).all()
    else:
        # For regular users, show approved replies and their own replies
        replies = Reply.objects.filter(Q(post=post, is_approved=True) | Q(post=post, user=request.user)).all()


    if request.method == "POST":
        form = ReplyForm(request.POST, request.FILES)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.save()
            messages.success(request, 'Your reply has been added!')
            return redirect('social')  # or redirect to the specific post
        else:
            messages.error(request, 'There was an error processing your reply. Please try again.')
            print("Form errors:", form.errors)  # Add a print statement to display form errors
    else:
        user_reply = Reply.objects.filter(post=post, user=request.user).first()
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
def submit_to_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    form = SubmissionForm(request.POST or None, request.FILES or None, assignment=assignment)
    
    # Check if the user is a superuser (adjust this as necessary for your logic)
    if request.user.is_superuser:
        messages.error(request, "Instructors cannot submit to assignments.")
        return redirect('social')  # Replace with your redirect target
    
    # Check if the assignment is still open for submissions
    if not assignment.is_submission_open():
        messages.error(request, "Submissions to this assignment are no longer accepted.")
        return redirect('social')  # Replace with your redirect target
    
    # Check if the user has already made a submission
    if Submission.objects.filter(assignment=assignment, user=request.user).exists():
        messages.error(request, "You have already submitted to this assignment.")
        return redirect('social')  # Replace with your redirect target

    if request.method == "POST":
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.assignment = assignment
            submission.save()
            messages.success(request, 'Your submission has been received!')
            return redirect('social')  # Replace with your redirect target
        else:
            messages.error(request, 'There was an error processing your submission. Please try again.')
            print("Form errors:", form.errors)
    else:
        form = SubmissionForm()

    context = {
        'submission_form': form,
        'assignment': assignment,
    }

    return render(request, 'assignments/submit_form.html', context)



@login_required
def upvote_reply(request, reply_id):
    print(f"Upvote reply function called for reply_id: {reply_id}")
    
    reply = get_object_or_404(Reply, id=reply_id)
    if reply:
        print(f"Found reply with ID: {reply_id} and content: {reply.content}")
    else:
        print(f"Reply with ID: {reply_id} not found!")
        return redirect('social')

    if not reply.votes.exists(request.user.id):
        print(f"User {request.user.username} has not yet upvoted reply {reply_id}")
        
        try:
            with transaction.atomic():
                reply.votes.up(request.user.id)
                print(f"Upvoted reply {reply_id} by user {request.user.username}")

                reply_owner_wallet_address = reply.user.wallet.wallet_address
                print(f"Reply owner's wallet address: {reply_owner_wallet_address}")
                
                try:
                    tx_hash = send_token_to_user(reply_owner_wallet_address)
                    print(f"Token sent to reply owner! Transaction hash: {tx_hash}")
                    messages.success(request, f'1 $SBVLT Token Rewarded to {reply.user.username}')
                except Exception as e:
                    print(f"Error sending token: {e}")
                    messages.error(request, 'An error occurred while sending the token reward. Please try again later.')
            
            upvote_event = UpvoteEvent(user=request.user, reply=reply, transaction_hash=tx_hash)
            upvote_event.save()
            print(f"Saved upvote event for user {request.user.username} on reply {reply_id}")

        except Exception as e:
            print(f"Error occurred: {e}")
            messages.error(request, 'An error occurred while processing your upvote. Please try again later.')

    else:
        print(f"User {request.user.username} has already upvoted reply {reply_id}")
        messages.warning(request, f'You have already upvoted this reply by {reply.user.username}!')

    return redirect('social')


@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)

    # Fetch all posts that are active and approved
    all_posts = Post.objects.filter(is_active=True, is_approved=True).order_by('-created_at')

    # Fetch only the replies of the profile user that are active
    user_replies = Reply.objects.filter(user=user, is_active=True)

    upvote_events = UpvoteEvent.objects.filter(user=user)
    user_debts = UserDebt.objects.filter(user=user)

    # Retrieve personal profile and NFT details for the user
    personal_profile = PersonalProfile.objects.filter(user=user).first()
    nft = NFT.objects.filter(user=user).first()

    # Group posts by UNIT
    posts_by_unit = defaultdict(list)
    for post in all_posts:
        posts_by_unit[post.unit.name].append(post)

    # Group replies by UNIT
    replies_by_unit = defaultdict(list)
    for reply in user_replies:
        replies_by_unit[reply.post.unit.name].append(reply)

    # Add print statements to check values
    print("User:", user)
    print("Posts:", posts_by_unit)
    print("Replies:", replies_by_unit)
    print("Upvote Events:", upvote_events)
    print("User Debts:", user_debts)
    print("Personal Profile:", personal_profile)
    print("NFT:", nft)
    print("Posts by Unit:", posts_by_unit)
    print("Replies by Unit:", replies_by_unit)

    unit_images = {unit.name: unit.unit_image.url if unit.unit_image else None for unit in Unit.objects.all()}

    print("Unit Images:", unit_images)

    assignments_by_unit = defaultdict(lambda: None)

    user_assignments = GradeAssignment.objects.filter(user=user)

    for assignment in user_assignments:
        assignments_by_unit[assignment.unit.name] = assignment


    context = {
        'profile_user': user,
        'posts_by_unit': dict(posts_by_unit),
        'replies_by_unit': dict(replies_by_unit),
        'unit_choices': dict(Unit.UNIT_CHOICES),
        'upvote_events': upvote_events,
        'user_debts': user_debts,
        'personal_profile': personal_profile,
        'nft': nft,
        'unit_images': unit_images,  # Add unit_images to the context
        'assignments_by_unit': assignments_by_unit,  # Add assignments_by_unit to the context
    }

    print(context)

    return render(request, 'socialmedia/user_profile.html', context)



@login_required
def approve_content(request, content_type, content_id):
    print(f"Approving content: type={content_type}, id={content_id}, user={request.user}")

    if not request.user.is_superuser:
        print("User not authorized to approve content.")
        return HttpResponseForbidden("You are not authorized to approve content.")

    unit_name = None
    if content_type == "post":
        content = get_object_or_404(Post, id=content_id)
        unit_name = content.unit.name
        print(f"Approving Post: Post ID {content_id}, Unit Name {unit_name}")
    elif content_type == "reply":
        content = get_object_or_404(Reply, id=content_id)
        unit_name = content.post.unit.name
        print(f"Approving Reply: Reply ID {content_id}, Unit Name {unit_name}")
    elif content_type == "assignment":
        content = get_object_or_404(Assignment, id=content_id)
        unit_name = content.unit.name
        print(f"Approving Assignment: Assignment ID {content_id}, Unit Name {unit_name}")
    else:
        print(f"Invalid content type: {content_type}")
        return HttpResponseBadRequest("Invalid content type.")

    content.is_approved = True
    content.save()
    print(f"Content Saved: {content_type.capitalize()} ID {content_id} approved")

    unit_full_name = dict(Unit.UNIT_CHOICES).get(unit_name, "Unknown Unit")
    print(f"Unit Full Name: {unit_full_name}")
    messages.success(request, f"{content_type.capitalize()} has been approved in {unit_full_name}!")

    print(f"Redirecting to unit: {unit_name}")
    if unit_name:
        return redirect('all_posts_by_unit', unit_name=unit_name)
    else:
        print("Unit name not found, redirecting to 'social'")
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



def assign_grade(request):
    if not request.user.is_superuser:
        return redirect('/')  # Redirect to homepage if user isn't superuser

    selected_user = None
    search_query = request.GET.get('user') or request.GET.get('user_dropdown')
    full_name = None
    image_ipfs_uri = None
    if search_query:
        selected_user_qs = User.objects.filter(username__icontains=search_query).select_related('personal_profile', 'nft')
        selected_user = selected_user_qs.first()
        if selected_user:
            full_name = selected_user.personal_profile.full_name if hasattr(selected_user, 'personal_profile') else None
            image_ipfs_uri = selected_user.nft.image_ipfs_uri if hasattr(selected_user, 'nft') else None


    if request.method == "POST" and selected_user:
        form = GradeAssignmentForm(request.POST)
        if form.is_valid():
            unit_value = form.cleaned_data.get('unit')
            grade = form.cleaned_data.get('grade')
            is_completed = form.cleaned_data.get('is_completed')

            # Check if a GradeAssignment already exists for this user and unit
            existing_assignment = GradeAssignment.objects.filter(user=selected_user, unit=unit_value).first()

            if existing_assignment:
                # Update the existing assignment
                existing_assignment.grade = grade
                existing_assignment.is_completed = is_completed
                existing_assignment.save()
                messages.success(request, f"Grade for {unit_value} has been successfully updated for {selected_user.username}!")
            else:
                # Create a new assignment
                grade_assignment = GradeAssignment(
                    user=selected_user,
                    unit=unit_value,
                    grade=grade,
                    is_completed=is_completed
                )
                grade_assignment.save()
                messages.success(request, f"Grade for {unit_value} has been assigned successfully to {selected_user.username}!")
            return redirect(f'{reverse("assign_grade")}?user_dropdown={selected_user.username}')
    else:
        # If this is a GET request, or if the form was invalid during a POST request
        existing_assignment = None
        if selected_user:
            existing_assignment = GradeAssignment.objects.filter(user=selected_user).first()

        form = GradeAssignmentForm(initial={
            'grade': existing_assignment.grade if existing_assignment else None,
            'is_completed': existing_assignment.is_completed if existing_assignment else False
        })

    all_users = User.objects.filter(is_superuser=False)
    all_units = Unit.objects.all()
    existing_assignments = GradeAssignment.objects.filter(user=selected_user) if selected_user else GradeAssignment.objects.none()
    assigned_units = existing_assignments.values_list('unit', flat=True)

    context = {
        'all_users': all_users,
        'selected_user': selected_user,
        'all_units': all_units,
        'existing_assignments': existing_assignments,
        'assigned_units': assigned_units,
        'form': form,
        'image_ipfs_uri': image_ipfs_uri,
        'full_name': full_name
    }

    return render(request, 'socialmedia/assign_grade.html', context)



@login_required
def assignment_list(request):
    units = Unit.objects.all()
    selected_unit_name = request.GET.get('unit', '')
    selected_unit = None
    selected_unit_assignments = None
    user_submissions = {}

    if request.user.is_superuser:
        if selected_unit_name:
            selected_unit = get_object_or_404(Unit, name=selected_unit_name)
            selected_unit_assignments = selected_unit.assignments.all().prefetch_related(
                Prefetch('submissions', queryset=Submission.objects.select_related('user__personal_profile'),
                         to_attr='all_submissions')
            )
    else:
        if selected_unit_name:
            selected_unit = get_object_or_404(Unit, name=selected_unit_name)
            assignments = selected_unit.assignments.all()
            for assignment in assignments:
                # Fetch submission for the user with related personal profile
                submission = assignment.submissions.filter(user=request.user).select_related('user__personal_profile').first()
                if submission:
                    user_submissions[assignment.id] = submission
            selected_unit_assignments = assignments  # List all assignments in the selected unit


    context = {
        'units': units,
        'selected_unit': selected_unit,
        'selected_unit_name': selected_unit_name,
        'user_submissions': user_submissions,
        'selected_unit_assignments': selected_unit_assignments,
        'is_superuser': request.user.is_superuser,
    }

    return render(request, 'socialmedia/assignment_list.html', context)



@login_required
def update_submission_status(request, submission_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    submission = get_object_or_404(Submission, id=submission_id)

    if request.method == 'POST':
        submission.admin_feedback = request.POST.get('admin_feedback', '')
        submission.grade = request.POST.get('grade', '-')
        tokens_sent = int(request.POST.get('tokens_sent', 0))  # Default to 0 if not provided
        action = request.POST.get('action')

        # Update the status based on action
        if action == 'accept':
            submission.status = 'accepted'
            if tokens_sent > 0:
                try:
                    tx_hash = send_token_to_user(submission.user.wallet.wallet_address, tokens_sent)
                    submission.token_tx_hash = tx_hash
                    submission.tokens_sent = tokens_sent
                except Exception as e:
                    print(f"Error sending tokens: {e}")
                    messages.error(request, "Failed to send tokens. Error: " + str(e))
            messages.success(request, 'Submission accepted and graded.')

        elif action == 'needs_action':
            submission.status = 'needs_action'
            if not submission.admin_feedback:
                messages.error(request, 'Feedback is required for further action.')
                return redirect(reverse('submission_detail', args=[submission_id]))
            messages.success(request, 'Feedback sent for further action.')

        else:
            messages.error(request, 'Invalid action.')

        submission.save()
        return redirect(reverse('submission_detail', args=[submission_id]))

    return render(request, 'submission_update.html', {'submission': submission})


@login_required
def resubmit_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, user=request.user)

    if request.method == 'POST':
        # Update the submission with the new data
        submission.content = request.POST.get('content')
        submission.image = request.FILES.get('image')
        submission.video_upload = request.FILES.get('video_upload')
        submission.file_upload = request.FILES.get('file_upload')
        submission.status = 'pending_review'

        # Increment the resubmitted_count
        submission.resubmitted_count += 1

        submission.save()

        messages.success(request, 'Your submission has been updated and resubmitted for review.')
        return redirect(reverse('submission_detail', args=[submission_id]))

    context = {'submission': submission}
    return render(request, 'socialmedia/resubmit_submission.html', context)




@login_required
def assignment_create(request):
    if not request.user.is_superuser:
        # Redirect non-superusers to the 'social' view
        return redirect('social')

    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.user = request.user
            assignment.save()
            # Redirect to a 'success' page or the social feed where the form is
            return redirect('social')
    else:
        form = AssignmentForm()

    return redirect('social')


@login_required
def assignment_edit(request, pk):  # Changed parameter name to pk for consistency
    assignment = get_object_or_404(Assignment, pk=pk)

    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to edit assignments.")
        return redirect('social')

    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, f"Assignment '{assignment.title}' updated successfully.")
            return redirect('social')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AssignmentForm(instance=assignment)

    context = {'form': form, 'assignment': assignment}
    return render(request, 'socialmedia/edit_assignment.html', context)


@login_required
def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    
    if request.user.is_superuser:
        assignment.delete()
        messages.success(request, f"Assignment '{assignment.title}' deleted successfully.")
        return redirect('social') 
    else:
        messages.error(request, 'You do not have permission to delete this assignment.')
        return redirect('social')


@login_required
def submission_detail(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    
    assignment = submission.assignment

    # Ensure that only the user who made the submission or a superuser can access the detail view
    if request.user != submission.user and not request.user.is_superuser:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied

    submission.file_name = os.path.basename(submission.file_upload.name)

    context = {
        'submission': submission,
        'assignment': assignment,  # Now the template has access to the assignment object
    }

    return render(request, 'socialmedia/submission_detail.html', context)


def all_assignments(request, unit_name):
    # Use the unit_name to filter assignments
    unit = get_object_or_404(Unit, name=unit_name)
    if request.user.is_superuser:
        # For superusers, display all assignments
        assignments = Assignment.objects.filter(unit=unit)
    else:
        # For regular users, display assignments that are active and approved
        assignments = Assignment.objects.filter(unit=unit, is_active=True, is_approved=True)


    return render(request, 'socialmedia/all_posts.html', {'assignments': assignments})



def send_token_to_user(user_eth_address, token_amount):
    
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
    
    INFURA_ENDPOINT = os.getenv('INFURA_ENDPOINT')
    w3 = Web3(Web3.HTTPProvider(INFURA_ENDPOINT))

    # Your server's Ethereum account
    sender_address = '0xB7a978C09f74bFCC872FCAdb98FFC8579BDC109E'
    private_key = os.getenv('PRIVATE_KEY')

    # Print statements for debugging
    print(f"Private Key: {private_key}")  # Ensure it prints a valid key
    print(f"Recipient: {user_eth_address}")  # Ensure the recipient address is correct
    print(f"Sender Address: {sender_address}")  # Check sender address too

    # Token details
    token_address = '0x452dd5D4F7e9df965589Df1904474F24Eb669E46'
    print(f"Contract Address: {token_address}")  # Ensure the token address is correct

    with open("token_abi.json", "r") as f:
        token_abi = json.load(f)

    # Connect to the token contract
    token_contract = w3.eth.contract(address=token_address, abi=token_abi)

    # Specify token amount to send
    amount = token_amount  # Use the passed amount

    # Build a transaction
    tx = token_contract.functions.transfer(user_eth_address, amount).buildTransaction({
        'chainId': 5,
        'gas': 150000,
        'gasPrice': w3.toWei('20', 'gwei'),
        'nonce': w3.eth.getTransactionCount(sender_address),
    })

    print(f"Transaction: {tx}")  # Printing out the entire transaction to check its values

    # Sign the transaction
    signed_tx = w3.eth.account.signTransaction(tx, private_key)

    # Send the transaction
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

    return tx_hash.hex()