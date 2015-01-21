from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _

try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
    get_user_model = lambda: User

from login_as import conf

is_superuser = lambda user: user.is_superuser


def _is_user_active(username):
    return get_user_model().objects.filter(username=username, is_active=True).exists()


@user_passes_test(is_superuser)
def login(request, username):
    authenticated = authenticate(from_user=request.user, to_username=username)
    if not authenticated:
        raise Http404

    if conf.LOGIN_ACTIVE_USERS_ONLY and not _is_user_active(username):
        raise Http404
    auth_login(request, authenticated)
    message = _("You are now logged in as %(username)s") % {'username': username}
    messages.success(request, message)
    return HttpResponseRedirect(conf.REDIRECT_AFTER_LOGIN)


class UserChooseView(ListView):
    model = get_user_model()
    template_name = 'login_as/chooser.html'

    @method_decorator(user_passes_test(is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserChooseView, self).dispatch(request, *args, **kwargs)


user_choose = UserChooseView.as_view()
