from django.contrib import admin
from .models import Post, Users, Message, Like, Follow, RequestLog, BlockedIP


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'user', 'content', 'created_at', 'updated_at', 'media')


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'recipient', 'timestamp')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'timestamp')


@admin.register(Follow)
class followAdmin(admin.ModelAdmin):
    list_display = ('following', 'follower', 'created_at')


@admin.register(RequestLog)
class RequestlogAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'timestamp', 'path', 'country', 'city']
    list_filter = ['ip_address']
    search_fields = ['id_address', 'city']


@admin.register(BlockedIP)
class BlockedIPAdmin(admin.ModelAdmin):
    list_display = ['ip_address']
