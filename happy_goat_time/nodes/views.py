from django.shortcuts import render
from django.views.generic import TemplateView, View

from .models import Node
# Create your views here.

from django.http import HttpResponse


class DashboardView(
        TemplateView):
    """
    Change the owner of an org
    """

    def get_fan_data(self):
        return 'off'

    def set_fan_speed_max(self):
        return 'off'

    def set_fan_speed_reg(self):
        return 'off'

    template_name = 'dashboard.jinja'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context.update({
            'nodes': Node.objects.all(),
            'get_fan_data': self.get_fan_data,
            'set_fan_speed_max': self.set_fan_speed_max,
            'set_fan_speed_reg': self.set_fan_speed_reg,
        })
        return context
