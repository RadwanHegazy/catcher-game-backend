from django.db import close_old_connections
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

@database_sync_to_async
def get_user(decoded_token):
    try:
        user = Token.objects.get(key=decoded_token)
        return user.user
   
    except Token.DoesNotExist:
        return AnonymousUser()

 
class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner
        
    async def __call__(self, scope, receive, send, *args, **kwargs):
        close_old_connections()
        
        token = dict(scope)['query_string'].decode('utf-8').split('=')[-1]
        
        user = await get_user(token)
        if user.is_authenticated:
            return await self.inner(dict(scope, user=user), receive, send, *args, **kwargs)
        return None