from celery import shared_task
from .models import Post, Users, RequestLog, SuspiciousIP
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now, timedelta


logger = logging.getLogger(__name__)


# Send Like Notification
@shared_task
def send_like_notification(post_id, user_id):
    try:
        post = Post.objects.get(post_id=post_id)
        liker = Users.objects.get(id=user_id)
        author = post.user
        logger.info(f"Notify {author.username}: {liker.username} liked your post '{post.content[:30]}'")
        return f"Notification sent to {author.username}"
    except Exception as e:
        logger.error(f"send_like_notification failed: {str(e)}")


# Task to Send follow notification
@shared_task
def send_follow_notification(follower_id, following_id):
    try:
        follower = Users.objects.get(id=follower_id)
        following = Users.objects.get(id=following_id)
        logger.info(f"Notify {following.username}: {follower.username} started following you")
        return f"Notification sent to {following.username}"
    except ObjectDoesNotExist:
        logger.warning(f"Follow notification failed: follower {follower_id} or following {following_id} not found.")
    except Exception as e:
        logger.error(f"send_follow_notification failed: {str(e)}")


# task to send message notification
@shared_task
def send_message_notification(user_id, recipient_id):
    try:
        user = Users.objects.get(id=user_id)
        recipient = Users.objects.get(id=recipient_id)
        logger.info(f"Notify {recipient.username} : {user.username} sent you a message")
        return f"Notification sent to {recipient.username}"
    except ObjectDoesNotExist:
        logger.warning(f"Message notification failed: sender {user_id} or recipient {recipient_id} not found.")
    except Exception as e:
        logger.error(f"send_message_notification failed: {str(e)}")


SENSITIVE_PATHS = ['/admin', '/login']


# Task to Flag Suspicious IP
@shared_task
def flag_suspicious_ips():
    one_hour_ago = now() - timedelta(hours=1)

    # Get all logs from the past hour
    recent_logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago)

    # Count requests per IP
    ip_counts = {}
    flagged_ips = set()

    for log in recent_logs:
        ip = log.ip_address
        ip_counts[ip] = ip_counts.get(ip, 0) + 1

        # Check for sensitive path access
        if log.path in SENSITIVE_PATHS:
            flagged_ips.add(ip)
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                defaults={'reason': f"Accessed sensitive path: {log.path}"}
            )

    # Flag IPs exceeding 100 requests/hour
    for ip, count in ip_counts.items():
        if count > 100 and ip not in flagged_ips:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                defaults={'reason': f"{count} requests in the past hour"}
            )
