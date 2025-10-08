from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Like, Follow, Message
from .tasks import (send_like_notification, send_follow_notification,
                    send_message_notification)


@receiver(post_save, sender=Like)
def like_created(sender, instance, created, **kwargs):
    if created:
        send_like_notification.delay(instance.post.id, instance.user.id)


@receiver(post_save, sender=Follow)
def follow_created(sender, instance, created, **kwargs):
    if created:
        send_follow_notification.delay(
            instance.follower.id, instance.following.id)


@receiver(post_save, sender=Message)
def message_created(sender, instance, created, **kwargs):
    if created:
        send_message_notification.delay(
            instance.user.id, instance.recipient.id)
