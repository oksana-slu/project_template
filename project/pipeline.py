from social_auth.utils import setting
from social_auth.models import User
from social_auth.backends.pipeline import warn_setting
from social_auth.signals import socialauth_not_registered


def create_user(backend, details, response, uid, username, user=None, *args,
                **kwargs):
    """Create user. Depends on get_username pipeline."""
    if user:
        return {'user': user}
    if not username:
        return None

    warn_setting('SOCIAL_AUTH_CREATE_USERS', 'create_user')

    if not setting('SOCIAL_AUTH_CREATE_USERS', True):
        # Send signal for cases where tracking failed registering is useful.
        socialauth_not_registered.send(sender=backend.__class__,
                                       uid=uid,
                                       response=response,
                                       details=details)
        return None

    email = details.get('email')
    if email:
        user = User.objects.filter(email=email)
        if user:
            user = user[0]
        else:
            user = User.objects.create_user(username=username, email=email)
    else:
        user = User.objects.create_user(username=username, email=email)
    return {
        'user': user,
        'is_new': True
    }
