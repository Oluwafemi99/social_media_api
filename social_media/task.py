from celery import shared_task
from .models import Post, Users


@shared_task
def send_like_notification(post_id, user_id):
    post = Post.objects.get(id=post_id)
    liker = Users.objects.get(id=user_id)
    author = post.user
    print(f"Notify {author.username}: {liker.username} liked your post '{post.content[:30]}'")


@shared_task
def send_follow_notification(follower_id, following_id):
    follower = Users.objects.get(id=follower_id)
    following = Users.objects.get(id=following_id)
    print(f"Notify {following.username}: {follower.username} started following you")


@shared_task
def send_message_notification(user_id, recipient_id):
    user = Users.objects.get(id=user_id)
    recipient = Users.objects.get(id=recipient_id)
    print(f"notify{recipient.username}: {user.username} Sent you a message")
