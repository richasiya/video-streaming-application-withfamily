from .models import SiteConfig
from django.db import OperationalError, ProgrammingError


def site_config(request):
    """Return the first SiteConfig instance (or defaults) to templates.

    This is defensive: if the DB isn't migrated yet or is otherwise unavailable
    we return safe defaults so the homepage can render without crashing.
    """
    try:
        config = SiteConfig.objects.first()
        if not config:
            return {'site_name': 'withfamily', 'site_logo': None}
        return {'site_name': config.site_name, 'site_logo': config.logo}
    except (OperationalError, ProgrammingError, Exception):
        # DB not ready or other runtime error — return sensible defaults
        return {'site_name': 'withfamily', 'site_logo': None}
