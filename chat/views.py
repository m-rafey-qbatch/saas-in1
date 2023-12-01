from django.shortcuts import render, redirect, get_object_or_404
from users.models import ChatRoom, Message
from .forms import ChatRoomForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

from django.db import IntegrityError

from django.contrib import messages

from .utils import get_total_unread_count


@login_required
def index(request):
    if request.method == "POST":
        form = ChatRoomForm(request.POST, user=request.user)

        # Check form validity
        if form.is_valid():

            # Compute the unique chat_id for the room
            participant_ids = sorted([participant.id for participant in form.cleaned_data['participants']] + [request.user.id])
            chat_id = '-'.join(map(str, participant_ids))
            existing_room = ChatRoom.objects.filter(chat_id=chat_id).first()

            if existing_room:
                # The chat room already exists, so show a message
                messages.warning(request, "Chatroom with these participants already exists.")
                return redirect('chat:index')

            chatroom = form.save(commit=False)
            chatroom.chat_id = chat_id

            try:
                chatroom.save()

                chatroom.participants.add(request.user)  # Add the logged-in user

                for participant in form.cleaned_data['participants']:  # Add the participants chosen from the form
                    chatroom.participants.add(participant)

                messages.success(request, "Chatroom created successfully!")
                return redirect('chat:index')

            except IntegrityError:
                # Handle the error, e.g., by showing an error message
                messages.error(request, "Please try again. Chatroom with these participants might already exist.")
                return redirect('chat:index')

        else:
            messages.error(request, "Not a valid chat room creation request. Please try again.")

    else:
        form = ChatRoomForm(user=request.user)

    user_chatrooms = ChatRoom.objects.filter(participants=request.user)

    chatrooms_with_details = []
    for chatroom in user_chatrooms:
        participants = chatroom.participants.all().exclude(id=request.user.id)
        # Calculate unread message count for the chatroom
        unread_count = Message.objects.filter(room=chatroom).exclude(sender=request.user).exclude(read_by=request.user).count()
        chatrooms_with_details.append((chatroom, participants, unread_count))

    print(chatrooms_with_details)

    return render(request, 'chat/index.html', {'chatrooms_with_details': chatrooms_with_details, 'form': form})


@login_required
def room(request, room_id):
    chatroom = get_object_or_404(ChatRoom, id=room_id)

    # Add print statements here
    print(f"Requested chatroom ID from URL: {room_id}")
    print(f"Fetched chatroom ID from database: {chatroom.id}")

    # Ensure the user is a participant of the chat room
    if request.user not in chatroom.participants.all():
        raise Http404("Chat room does not exist or you don't have permission to view it.")
    
    user_chatrooms = ChatRoom.objects.filter(participants=request.user)

    # Fetch all chatrooms the user is part of and calculate unread message count
    chatrooms_with_participants_and_unread_count = []
    for user_chatroom in user_chatrooms:
        participants = user_chatroom.participants.all().exclude(id=request.user.id)
        unread_count = Message.objects.filter(room=user_chatroom).exclude(sender=request.user).exclude(read_by=request.user).count()

        # Get the timestamp of the latest message in the chatroom
        last_message = Message.objects.filter(room=user_chatroom).order_by('-timestamp').first()
        last_active = last_message.timestamp if last_message else None

        chatrooms_with_participants_and_unread_count.append((user_chatroom, participants, unread_count, last_active))

    texts = Message.objects.filter(room=chatroom).order_by('timestamp')[:50]
    print(texts.query)  # This will print the SQL query
    print(texts)  # This will print the fetched messages

    # Mark the messages as read by the current user
    print(f"Fetching messages for chatroom: {chatroom.id}, User: {request.user.username}")
    for text in texts:
        text.read_by.add(request.user)
        text.save()

    total_unread = get_total_unread_count(request.user)

    context = {
        'chatroom': chatroom,
        'texts': texts,
        'chatrooms_with_participants_and_unread_count': chatrooms_with_participants_and_unread_count,
        'total_unread': total_unread
    }

    return render(request, 'chat/room.html', context)
