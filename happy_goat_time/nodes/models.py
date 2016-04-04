from __future__ import unicode_literals

from django.db import models
from macaddress.fields import MACAddressField
from django.db.models import permalink, Count

# Create your models here.
class Node(models.Model):
    name = models.CharField(max_length=200)
    # mac_address = MACAddressField(blank=True, integer=False)
    mac_address = models.CharField(max_length=200)
    installed_date = models.DateTimeField('date published')

    def url_arguments(self):
        return {}

    @permalink
    def get_dashboard_url(self):
        return ('nodes:dashboard', (), self.url_arguments())
