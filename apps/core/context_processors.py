from .models import SiteSettings

def site_settings_context(request):
    try:
        settings = SiteSettings.get_settings()
    except Exception:
        settings = None
    return {
        'site_settings': settings,
    }
