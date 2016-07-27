def recaptcha(request):
    """context processor to add alerts to the site"""
    from django.conf import settings

    return {
        '6LfquyQTAAAAAMfQw9QvUFXFLYyk7Xz29qnAUPlX': settings.GOOGLE_RECAPTCHA_SITE_KEY,
    }
