import graphene
import graphql_jwt
from .mutation import (CreateComment, CreatePost, CreateUser,
                       UnfollowUser, UnlikePost, UpdatePost, FollowUser,
                       SharePost, LikePost, DeleteComment, DeletePost)
from .query import FeedQuery, InteractionQuery


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
    delet_post = DeletePost.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class Query(FeedQuery, InteractionQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(mutation=Mutation, query=Query)
