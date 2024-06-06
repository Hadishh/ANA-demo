from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()

@database_sync_to_async
def get_user(token_key):
    try:
        token = AccessToken(token_key)
        user = User.objects.get(id=token['user_id'])
        return user
    except (User.DoesNotExist, TokenError, InvalidToken):
        print("TOOOOOOOOOOOOOOOOO")
        return AnonymousUser()

class JWTAuthMiddleware:
    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app
    
    async def __call__(self, scope, receive, send):
        # Retrieve the JWT token from the query string
        token_key = dict((x.split('=') for x in scope['query_string'].decode().split("&"))).get('token', None)
        print(token_key)
        scope['user'] = await get_user(token_key)
        return await self.app(scope, receive, send)
