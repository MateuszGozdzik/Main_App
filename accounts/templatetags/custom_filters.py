from django import template
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

USER = get_user_model()

register = template.Library()


@register.filter(name="in_group")
def in_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return False
    return group in user.groups.all()


@register.filter(name="friend")
def friend(user, friend_id):
    try:
        friend = USER.objects.get(id=friend_id)
    except USER.DoesNotExist:
        return False
    return friend in user.friends.filter(id=friend.id)


@register.filter(name="requested_friend")
def requested_friend(user, friend_id):
    try:
        friend = USER.objects.get(id=friend_id)
    except USER.DoesNotExist:
        return False
    return friend in user.requested_friends.filter(id=friend.id)


@register.filter(name="unread_notifications")
def unread_notifications(user):
    try:
        notification_exists = user.notifications.filter(read=False).exists()
    except USER.DoesNotExist:
        return False
    return notification_exists
