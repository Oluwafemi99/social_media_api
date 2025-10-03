import graphene
from .types import (PostTypes, UserTypes, FollowTypes,
                    CommentTypes, ShareTypes, LikeTypes)
from django.contrib.auth import get_user_model
from .models import Post, Follow, Share, Like, Comment
from django.core.exceptions import ValidationError


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserTypes)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, email, password):
        try:
            user = get_user_model()(username=username, email=email)
            user.set_password(password)
            user.save()
            return CreateUser(user=user, ok=True)
        except ValidationError as e:
            return CreateUser(ok=False, error=str(e))


class CreatePost(graphene.Mutation):
    post = graphene.Field(PostTypes)
    ok = graphene.Boolean
    error = graphene.String()

    class Arguments:
        content = graphene.String(required=True)
        media = graphene.JSONString(required=True)

    def mutate(self, info, content, media=None):
        try:
            user = info.context.user
            if user.is_anonymous:
                raise Exception('Authentication required')
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
        media = graphene.JSONString(required=True)

    def mutate(self, info, post_id, content=None, media=None):
        try:

            user = info.context.user
            post = Post.objects.get(pk=post_id)
            if post.user != user:
                raise Exception('Not Authorised')
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
                raise ValidationError('Not Authorised')
            post.delete()
            return DeletePost(ok=True)
        except ValidationError as e:
            return DeletePost(ok=False, error=str(e))


class FollowUser(graphene.Mutation):
    follow = graphene.Field(FollowTypes)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        user_id = graphene.ID(required=True)

    def mutate(self, info, user_id):
        try:
            follower = info.context.user
            if str(follower.id) == user_id:
                raise Exception('Cannot Follow Yourself')
            follow, _ = Follow.objects.get_or_create(follower=follower,
                                                     following_id=user_id)
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
            return UnfollowUser(ok=True)
        except ValidationError as e:
            return UnfollowUser(ok=False, error=str(e))


class LikePost(graphene.Mutation):
    like = graphene.Field(LikeTypes)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        post_id = graphene.UUID(required=True)

    def mutate(self, info, post_id):
        try:
            user = info.context.user
            post = Post.objects.get(pk=post_id)
            like, _ = Like.objects.get_or_create(user=user, post=post)
            return LikePost(ok=True, like=like)
        except ValidationError as e:
            return LikePost(ok=False, error=str(e))


class UnlikePost(graphene.Boolean):
    like = graphene.Field(LikeTypes)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        post_id = graphene.UUID(required=True)

    def mutate(self, info, post_id):
        try:
            user = info.context.user
            Like.objects.filter(user=user, like_id=post_id).delete()
            return UnlikePost(ok=True)
        except ValidationError as e:
            return UnlikePost(ok=False, error=str(e))


class CreateComment(graphene.Mutation):
    comment = graphene.Field(CommentTypes)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        post_id = graphene.UUID(required=True)
        text = graphene.String(required=True)

    def mutate(self, info, post_id, text):
        try:
            user = info.context.user
            post = Post.objects.get(pk=post_id)
            comment = Comment.objects.get_or_create(user=user,
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

    def mutate(self, info, post_id):
        try:
            user = info.context.user
            Comment.objects.filter(user=user, comment_id=post_id).delete()
            return DeleteComment(ok=True)
        except ValidationError as e:
            return DeleteComment(ok=False, error=str(e))


class SharePost(graphene.Mutation):
    share = graphene.Field(ShareTypes)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        post_id = graphene.UUID(required=True)
        shared_to = graphene.String(required=True)

    def mutate(self, info, post_id, shared_to):
        try:
            user = info.context.user
            post = Post.objects.get(pk=post_id)
            share = Share.objects.get_or_create(user=user, post=post,
                                                shared_to=shared_to)
            return SharePost(share=share, ok=True)
        except ValidationError as e:
            return SharePost(ok=False, error=str(e))
