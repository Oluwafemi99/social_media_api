from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


# Create your models here.
class Users(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.username


class Post(models.Model):
    post_id = models.UUIDField(primary_key=True, db_index=True,
                               editable=False, default=uuid.uuid4)
    user = models.ForeignKey(Users, on_delete=models.CASCADE,
                             related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    media = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.user}: {self.content[:30]}"


class Follow(models.Model):
    follower = models.ForeignKey(Users, on_delete=models.CASCADE,
                                 related_name='following')
    following = models.ForeignKey(Users, on_delete=models.CASCADE,
                                  related_name='follower')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower.username} is following {
            self.following.username}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comment')
    user = models.ForeignKey(Users, on_delete=models.CASCADE,
                             related_name='user')
    text = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='likes')
    user = models.ForeignKey(Users, on_delete=models.CASCADE,
                             related_name='likes')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"


class Share(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='share')
    user = models.ForeignKey(Users, on_delete=models.CASCADE,
                             related_name='share')
    share_to = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} shared to {self.share_to[:30]}"


class Message(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE,
                             related_name='sent_messages')
    text = models.TextField()
    recipient = models.ForeignKey(Users, on_delete=models.CASCADE,
                                  related_name='recieved_messages')
    timestamp = models.DateTimeField(auto_now_add=True)
