# context_processors.py
from .utils import get_total_unread_count

def total_unread_count(request):
    if request.user.is_authenticated:
        total_unread = get_total_unread_count(request.user)
        return {'total_unread_messages': total_unread}
    return {}
