from graphene_django.types import DjangoObjectType
from .models import Users, Post, Follow, Comment, Share, Like, Message
import graphene

""""
Creating Object Type for Comment, Users, Post, Follow, Share, like, Message
"""


class UserTypes(DjangoObjectType):

    class Meta:
        model = Users
        fields = '__all__'


class PostTypes(DjangoObjectType):

    class Meta:
        model = Post
        fields = '__all__'


class FollowTypes(DjangoObjectType):

    class Meta:
        model = Follow
        fields = '__all__'


class CommentTypes(DjangoObjectType):

    class Meta:
        model = Comment
        fields = '__all__'


class LikeTypes(DjangoObjectType):

    class Meta:
        model = Like
        fields = '__all__'


class ShareTypes(DjangoObjectType):

    class Meta:
        model = Share
        fields = '__all__'


class MessageTypes(DjangoObjectType):

    class Meta:
        model = Message
        fields = '__all__'

    user = graphene.Field(lambda: UserTypes)
    recipient = graphene.Field(lambda: UserTypes)

    def resolve_user(self, info):
        return self.user

    def resolve_recipient(self, info):
        return self.recipient
