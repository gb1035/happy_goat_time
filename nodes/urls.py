from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', view =views.DashboardView.as_view(), name='dashboard'),
    url(r'^(?P<node_pk>[\d]+)/$',
        view=views.NodeDetailsView.as_view(),
        name='node_detail'),
]
