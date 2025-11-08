from .models import SiteSetting


def site_settings(request):
    """
    Context processor to make site settings available in all templates
    """
    settings = SiteSetting.get_settings()
    return {
        'site_settings': settings,
    }
