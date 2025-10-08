import graphene
from .types import (PostTypes, UserTypes, FollowTypes,
                    CommentTypes, ShareTypes, LikeTypes,
                    MessageTypes)
from django.contrib.auth import get_user_model
from .models import Post, Follow, Share, Like, Comment, Message, Users
from django.core.exceptions import ValidationError
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

""""
Mutation for CreateUser, UpdateUser, CreatePost, UpdatePost
DeletePost, createComment, LikePost, UnlikePost, SendMessage
FollowUser, UnFollowUser
"""


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserTypes)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        bio = graphene.String(required=False)
        profile_picture = graphene.JSONString(required=False)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    def mutate(self, info, username, email, password, first_name, last_name,
               bio=None, profile_picture=None, ):
        User = get_user_model()
        try:
            user = User(username=username, email=email, bio=bio,
                        profile_picture=profile_picture, first_name=first_name,
                        last_name=last_name)
            user.set_password(password)
            user.save()
            return CreateUser(user=user, ok=True)
        except ValidationError as e:
            return CreateUser(ok=False, error=str(e))


class UpdateUser(graphene.Mutation):
    user = graphene.Field(UserTypes)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        bio = graphene.String(required=False)
        profile_picture = graphene.String(required=False)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)

    def mutate(self, info, bio=None, profile_picture=None,
               last_name=None, first_name=None):
        try:
            user = info.context.user
            if user.is_anonymous:
                raise GraphQLError("Authentication required")
            if bio is not None:
                user.bio = bio
            if profile_picture is not None:
                user.profile_picture = profile_picture
            if last_name is not None:
                user.last_name = last_name
            if first_name is not None:
                user.first_name = first_name
            user.save()
            return UpdateUser(ok=True, user=user)
        except Exception as e:
            return UpdateUser(ok=False, error=str(e))


class CreatePost(graphene.Mutation):
    post = graphene.Field(PostTypes)
    ok = graphene.Boolean
    error = graphene.String()

    class Arguments:
        content = graphene.String(required=True)
        media = graphene.JSONString()

    def mutate(self, info, content, media=None):
        try:
            user = info.context.user
            if user.is_anonymous:
                raise GraphQLError('Authentication required')
            post = Post.objects.create(user=user, content=content, media=media)
            return CreatePost(post=post)
        except ValidationError as e:
            return CreatePost(ok=False, error=str(e))


class UpdatePost(graphene.Mutation):
    post = graphene.Field(PostTypes)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        post_id = graphene.UUID(required=True)
        content = graphene.String(required=True)
        media = graphene.JSONString()

    def mutate(self, info, post_id, content=None, media=None):
        try:

            user = info.context.user
            post = Post.objects.get(pk=post_id)
            if post.user != user:
                raise GraphQLError('Not Authorised')
            if content:
                post.content = content
            if media:
                post.media = media
            post.save()
            return UpdatePost(post=post)
        except ValidationError as e:
            return UpdatePost(ok=False, error=str(e))


class DeletePost(graphene.Mutation):
    post = graphene.Field(PostTypes)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        post_id = graphene.UUID(required=True)

    def mutate(self, info, post_id):
        try:
            user = info.context.user
            post = Post.objects.get(pk=post_id)
            if post.user != user:
                raise GraphQLError('Not Authorised')
            post.delete()
            print("post deleted succesfully")
            return DeletePost(ok=True)
        except ValidationError as e:
            return DeletePost(ok=False, error=str(e))


class SendMessage(graphene.Mutation):
    message = graphene.Field(MessageTypes)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        recipient_id = graphene.ID(required=True)
        text = graphene.String(required=True)

    def mutate(self, info, recipient_id, text):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Authentication Required")

        # Check if sender follows recipient
        if not Follow.objects.filter(follower=user,
                                     following_id=recipient_id).exists():
            raise ValidationError("You can only message users you follow")

        recipient = Users.objects.get(id=recipient_id)
        message, _ = Message.objects.get_or_create(
            user=user, recipient=recipient, text=text)
        print("message sent")
        return SendMessage(message=message, ok=True)


class FollowUser(graphene.Mutation):
    follow = graphene.Field(FollowTypes)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        user_id = graphene.ID(required=True)

    def mutate(self, info, user_id):
        follower = info.context.user

        # Check for authentication
        if follower.is_anonymous:
            raise GraphQLError("Authentication required to follow users.")

        # Prevent self-following
        if str(follower.id) == str(user_id):
            raise GraphQLError("You cannot follow yourself.")

        try:
            follow, _ = Follow.objects.get_or_create(
                follower=follower,
                following_id=user_id
            )
            return FollowUser(ok=True, follow=follow)
        except ValidationError as e:
            return FollowUser(ok=False, error=str(e))


class UnfollowUser(graphene.Mutation):
    follow = graphene.Field(FollowTypes)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        user_id = graphene.ID(required=True)

    def mutate(self, info, user_id):
        try:
            follower = info.context.user
            Follow.objects.filter(follower=follower,
                                  following_id=user_id).delete()
            print("successfully unfollowed")
            return UnfollowUser(ok=True)
        except ValidationError as e:
            return UnfollowUser(ok=False, error=str(e))


class LikePost(graphene.Mutation):
    like = graphene.Field(LikeTypes)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        post_id = graphene.UUID(required=True)

    @login_required
    def mutate(self, info, post_id):
        try:
            user = info.context.user
            post = Post.objects.get(pk=post_id)
            like, _ = Like.objects.get_or_create(user=user, post=post)
            return LikePost(ok=True, like=like)
        except ValidationError as e:
            return LikePost(ok=False, error=str(e))


class UnlikePost(graphene.Mutation):
    like = graphene.Field(LikeTypes)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        post_id = graphene.UUID(required=True)

    def mutate(self, info, post_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Authentication required")

        try:
            like = Like.objects.filter(user=user, post_id=post_id).first()
            if like:
                like.delete()
                return UnlikePost(ok=True)
            else:
                return UnlikePost(ok=False, error="Like not found")
        except Exception as e:
            return UnlikePost(ok=False, error=str(e))


class CreateComment(graphene.Mutation):
    comment = graphene.Field(CommentTypes)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        post_id = graphene.UUID(required=True)
        text = graphene.String(required=True)

    @login_required
    def mutate(self, info, post_id, text):
        try:
            user = info.context.user
            post = Post.objects.get(pk=post_id)
            comment, _ = Comment.objects.get_or_create(user=user,
                                                       post=post, text=text)
            return CreateComment(comment=comment, ok=True)
        except ValidationError as e:
            return CreateComment(ok=False, error=str(e))


class DeleteComment(graphene.Mutation):
    comment = graphene.Field(CommentTypes)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        post_id = graphene.UUID(required=True)

    @login_required
    def mutate(self, info, post_id):
        try:
            user = info.context.user
            Comment.objects.filter(user=user, id=post_id).delete()
            return DeleteComment(ok=True)
        except ValidationError as e:
            return DeleteComment(ok=False, error=str(e))


class SharePost(graphene.Mutation):
    share = graphene.Field(ShareTypes)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        post_id = graphene.UUID(required=True)
        share_to = graphene.String(required=True)  # could be a username or "feed"

    @login_required
    def mutate(self, info, post_id, share_to):
        user = info.context.user

        try:
            post = Post.objects.get(pk=post_id)

            # Share to own feed
            if share_to.lower() == "feed":
                share, _ = Share.objects.get_or_create(
                    user=user, post=post, share_to="feed")
                return SharePost(share=share, ok=True)

            # Share to a followed user
            try:
                target_user = Users.objects.get(username=share_to)
            except Users.DoesNotExist:
                return SharePost(ok=False, error="Target user does not exist.")

            is_following = Follow.objects.filter(
                follower=user, following=target_user).exists()
            if not is_following:
                return SharePost(ok=False, error="You can only share posts with users you follow.")

            share, _ = Share.objects.get_or_create(
                user=user, post=post, share_to=target_user.username)
            return SharePost(share=share, ok=True)

        except ValidationError as e:
            return SharePost(ok=False, error=str(e))
        except Exception as e:
            return SharePost(ok=False, error="Unexpected error: " + str(e))
