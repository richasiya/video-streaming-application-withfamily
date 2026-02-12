from django import template

register = template.Library()

PLAN_RANK = {
    'free': 0,
    'basic': 1,
    'premium': 2,
}


@register.filter
def can_access(user, content):
    if not user or not getattr(user, 'is_authenticated', False):
        return False
    profile = getattr(user, 'userprofile', None)
    if not profile:
        return False
    return PLAN_RANK.get(profile.subscription, 0) >= PLAN_RANK.get(content.access_level, 0)
