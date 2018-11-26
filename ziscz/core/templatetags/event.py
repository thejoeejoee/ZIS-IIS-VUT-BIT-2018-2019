# coding=utf-8
from __future__ import unicode_literals

from django import template
from django.contrib.auth.models import User
from django.utils import timezone

from ziscz.core.models.base import BaseEventModel

register = template.Library()


@register.filter
def can_mark_as_done(event: BaseEventModel, user: User):
    if event.done:
        return False

    if user.has_perms(('core.change_cleaning', 'core.change_feeding')):
        return True

    if event.end > timezone.now():
        return False

    if not hasattr(user, 'person_user'):
        return False

    if user.has_perm(
            '.'.join((
                    'core',
                    BaseEventModel.PERMISSION_CAN_MARK_OWN_EVENT_AS_DONE
            ))
    ) and user.person_user in event.get_executors():
        return True

    return False
