from graphene_django.types import DjangoObjectType
from .models import Users, Post, Follow, Comment, Share, Like


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
