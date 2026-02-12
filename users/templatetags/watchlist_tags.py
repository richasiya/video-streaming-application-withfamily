from django import template
from users.models import Watchlist

register = template.Library()


@register.filter
def in_watchlist(user, content):
    if not user or not getattr(user, "is_authenticated", False):
        return False
    return Watchlist.objects.filter(user=user, content=content).exists()
