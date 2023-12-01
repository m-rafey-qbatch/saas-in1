from users.models import ChatRoom, Message

def get_total_unread_count(user):
    user_chatrooms = ChatRoom.objects.filter(participants=user)
    total_unread = 0
    for user_chatroom in user_chatrooms:
        unread_count = Message.objects.filter(room=user_chatroom).exclude(sender=user).exclude(read_by=user).count()
        total_unread += unread_count
    return total_unread
