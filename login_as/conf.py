from django.conf import settings

REDIRECT_AFTER_LOGIN = getattr(settings, 'LOGIN_AS_REDIRECT_AFTER_LOGIN', '/')
LOGIN_ACTIVE_USERS_ONLY = getattr(settings, 'LOGIN_AS_LOGIN_ACTIVE_USERS_ONLY', False)
