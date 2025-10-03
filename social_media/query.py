import graphene
from .models import Post, Comment, Like, Follow
from .types import PostTypes, CommentTypes, LikeTypes


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
            posts = posts.filter(timestamp__date=date)
        return posts.order_by('-timestamp')


class InteractionQuery(graphene.ObjectType):
    comments = graphene.List(
        CommentTypes, post_id=graphene.UUID(required=True))
    likes = graphene.List(LikeTypes, post_id=graphene.UUID(required=True))

    def resolve_comments(self, info, post_id):
        return Comment.objects.filter(post_id=post_id)

    def resolve_likes(self, info, post_id):
        return Like.objects.filter(post_id=post_id)
