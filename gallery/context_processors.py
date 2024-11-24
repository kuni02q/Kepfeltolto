#context_processors.py
from django.contrib.auth.models import User


def unread_messages_processor(request):
    if request.user.is_authenticated:
        unread_count = request.user.received_messages.filter(is_read=False).count()
    else:
        unread_count = 0
    return {'unread_count': unread_count}
