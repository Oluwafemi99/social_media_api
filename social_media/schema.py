import graphene
from .mutation import (CreateComment, CreatePost, CreateUser,
                       UnfollowUser, UnlikePost, UpdatePost, FollowUser,
                       SharePost, LikePost, DeleteComment, DeletePost,
                       UpdateUser, SendMessage,)
from .query import FeedQuery, InteractionQuery, MessageQuery
from . auth import LogoutUser, LoginUser, RefreshTokenMutation

""""
Mutation and Query for Schema
"""


class Mutation(graphene.ObjectType):
    create_comment = CreateComment.Field()
    create_post = CreatePost.Field()
    create_user = CreateUser.Field()
    unfollow_user = UnfollowUser.Field()
    unlike_post = UnlikePost.Field()
    update_post = UpdatePost.Field()
    follow_user = FollowUser.Field()
    share_post = SharePost.Field()
    like_post = LikePost.Field()
    delete_comment = DeleteComment.Field()
    delete_post = DeletePost.Field()
    update_user = UpdateUser.Field()
    send_message = SendMessage.Field()
    logout_user = LogoutUser.Field()
    login_user = LoginUser.Field()
    refresh_token = RefreshTokenMutation.Field()


class Query(FeedQuery, InteractionQuery, MessageQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(mutation=Mutation, query=Query)
