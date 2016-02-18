from braces.views import AllVerbsMixin, AnonymousRequiredMixin
from class_based_auth_views.views import LoginView as CBLoginView, LogoutView as CBLogoutView
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, View
from django.template import loader, RequestContext
from django import http

from .helpers import *

# from .forms import AuthenticationForm


# root view of site
# class LoginView(
#         AnonymousRequiredMixin,
#         CBLoginView):
#     """
#     Redirects to an organization or group if viewed when logged in
#     """
#     template_name = "login.jinja"
#     form_class = AuthenticationForm
#     success_url = None

#     def get_success_url(self):
#         """
#         LOGIN_REDIRECT_URL is set to None so super can return None, used to
#         redirect to an appropriate landing page for logging in user.
#         x users who are attached to a group go to it's detail page
#         - users who are organization owners land on it's overview page
#         - users who have access to FLAs are redirected to it's latest download,
#           as a fall back they ar eredirected to their fla list page.
#         By default it should honor any ?next=/page/ requests before
#         forwarding to a detail page
#         """
#         redirect_to = super(LoginView, self).get_success_url()
#         if not redirect_to:
#             redirect_to = self.request.user.profile.get_login_redirect_url()
#             if not redirect_to:
#                 return reverse_lazy('profile:fla_list')

#         return redirect_to

#     def get_authenticated_redirect_url(self):
#         return self.get_success_url()


# class LogoutView(CBLogoutView):
#     """Just get out"""
#     def get(self, *args, **kwargs):
#         return self.post(*args, **kwargs)


class FanView(
        TemplateView):
    """
    Change the owner of an org
    """

    def get_fan_data(self):
        return 'off'

    def set_fan_speed_max(self, ):
        return 100

    def set_fan_speed_reg(self, ):
        return 10

    template_name = 'fans.jinja'

    def get_context_data(self, **kwargs):
        context = super(FanView, self).get_context_data(**kwargs)
        context.update({
            'get_fan_data': self.get_fan_data,
            'set_fan_speed_max': self.set_fan_speed_max,
            'set_fan_speed_reg': self.set_fan_speed_reg,
        })
        return context
