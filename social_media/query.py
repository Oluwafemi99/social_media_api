import graphene
from .models import Post, Comment, Like, Follow, Message, Users
from .types import PostTypes, CommentTypes, LikeTypes, MessageTypes, UserTypes
from graphql import GraphQLError
from django.db.models import Q


class FeedQuery(graphene.ObjectType):
    feed = graphene.List(PostTypes, search=graphene.String(),
                         date=graphene.String())

    def resolve_feed(self, info, search=None, date=None):
        user = info.context.user
        followed_ids = Follow.objects.filter(follower=user).values_list(
            'following_id', flat=True)
        posts = Post.objects.filter(user_id__in=followed_ids)
        if search:
            posts = posts.filter(content__icontains=search)
        if date:
            posts = posts.filter(created_at__date=date)
        return posts.order_by('-created_at')


class InteractionQuery(graphene.ObjectType):
    comments = graphene.List(
        CommentTypes, post_id=graphene.UUID(required=True))
    likes = graphene.List(LikeTypes, post_id=graphene.UUID(required=True))
    all_users = graphene.List(UserTypes)
    all_posts = graphene.List(PostTypes)

    def resolve_comments(self, info, post_id):
        return Comment.objects.filter(post_id=post_id)

    def resolve_likes(self, info, post_id):
        return Like.objects.filter(post_id=post_id)

    def resolve_all_users(self, info):
        return Users.objects.all()

    def resolve_all_posts(self, info):
        return Post.objects.select_related('user').all()


class MessageQuery(graphene.ObjectType):
    messages = graphene.List(
        MessageTypes,
        recipient_id=graphene.ID(),
        user_id=graphene.ID()
    )

    def resolve_messages(self, info, recipient_id=None, user_id=None):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Authentication required")

        # Base queryset: messages where current user is sender or recipient
        queryset = Message.objects.filter(Q(user=user) | Q(recipient=user))

        if recipient_id:
            queryset = queryset.filter(recipient_id=recipient_id)
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        return queryset.order_by("-timestamp")
