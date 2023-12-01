from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.sessions.models import Session
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model


User = get_user_model()

class ChatAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Get the user from the session (if available)
        user = await database_sync_to_async(self.get_user_from_scope)(scope)
        scope['user'] = user
        return await super().__call__(scope, receive, send)

    def get_user_from_scope(self, scope):
        try:
            session_key = scope['session'].session_key
            session = Session.objects.get(session_key=session_key)
            user_id = session.get_decoded().get('_auth_user_id')
            if user_id:
                return User.objects.get(id=user_id)
        except (Session.DoesNotExist, User.DoesNotExist):
            pass
        return AnonymousUser()
