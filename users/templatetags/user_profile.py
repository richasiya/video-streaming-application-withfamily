from django import template

register = template.Library()


@register.filter
def safe_profile(user):
    if not user or not getattr(user, "is_authenticated", False):
        return None
    try:
        return user.userprofile
    except Exception:
        return None
