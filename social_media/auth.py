import graphene
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

""""
Mutation for User's Login Logout And RefreshToken Using
simple Jwt
"""


class LoginUser(graphene.Mutation):
    access = graphene.String()
    refresh = graphene.String()
    error = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        user = authenticate(username=username, password=password)
        if user is None:
            return LoginUser(error="Invalid credentials")

        refresh = RefreshToken.for_user(user)
        return LoginUser(
            access=str(refresh.access_token), refresh=str(refresh))


class RefreshTokenMutation(graphene.Mutation):
    access = graphene.String()
    refresh = graphene.String()
    error = graphene.String()

    class Arguments:
        refresh_token = graphene.String(required=True)

    def mutate(self, info, refresh_token):
        try:
            refresh = RefreshToken(refresh_token)
            new_refresh = refresh.rotate()
            return RefreshTokenMutation(
                access=str(new_refresh.access_token),
                refresh=str(new_refresh),
            )
        except TokenError:
            return RefreshTokenMutation(
                error="Invalid or expired refresh token")


class LogoutUser(graphene.Mutation):
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        refresh_token = graphene.String(required=True)

    def mutate(self, info, refresh_token):
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            print("logged out successfully")
            return LogoutUser(ok=True)
        except Exception as e:
            return LogoutUser(ok=False, error=str(e))
