# http://stockrt.github.io/p/emulating-a-browser-in-python-with-mechanize/

import mechanize
import cookielib
import urllib


import re
import ipdb as ipdb_module
from dateutil import tz
import simplejson

from datetime import datetime

import arrow as arrow_module
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
from django.db.models import Model
from django.forms.models import model_to_dict
from django.template import Template, Context
from django.template.defaultfilters import date
from django.utils import timezone
from django.utils.safestring import mark_safe
import jinja2
from jingo import register
from django_select2.templatetags.django_select2_tags import import_js, import_css
import pytz

import decimal

@register.function
def chart_header_js():
    # Debug versions of libraries loaded
    # debug_min = '.min' if not settings.DEBUG else ''
    debug_src = '' if not settings.DEBUG else '.src'
    header_js = [
        '<script src="%s" type="text/javascript"></script>\n' % h for h in
        (
            "{}highcharts/highcharts{}.js".format(settings.STATIC_URL, debug_src),
        )
    ]
    return mark_safe(header_js + '\n')


@register.function
def static(path):
    return staticfiles_storage.url(path)


@register.function
def now(format_string):
    return date(timezone.now(), format_string)


@register.filter
@jinja2.contextfilter
def arrow(context, time):
    arrow_time, desired_tz = arrow_context(context, time)
    return arrow_time


@register.function
def ipdb():
    ipdb_module.set_trace()
    return


@register.filter
def ipdb(element):
    ipdb_module.set_trace()
    return element


@register.function
@jinja2.contextfunction
def crispy(context, form, helper=None, template_pack='bootstrap3', **kwargs):
    mini_template = (
        '{{% load crispy_forms_tags %}}{{% crispy form "{0}" %}}'.format(template_pack))
    t = Template(mini_template)
    context = Context(dict(context))
    context.update({'form': form})
    return t.render(context)


@register.filter
@jinja2.evalcontextfilter
def nl2br(eval_ctx, value):
    _paragraph_re = re.compile(r'(?:\r\n|\r(?!\n)|\n){2,}')
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace(u'\n', jinja2.Markup('<br>\n'))
                                         for p in _paragraph_re.split(value))
    if eval_ctx.autoescape:
        result = jinja2.Markup(result)
    return result


@register.filter
def byte_array_to_hex(value):
    # takes an array of 8 bit integers and expresses the values in hex
    # used in table rendering
    return " ".join(["%02x" % c for c in value])


@register.function
def select2_css(light=0):
    return jinja2.Markup(import_css(light))


@register.function
def select2_js(light=0):
    return jinja2.Markup(import_js(light))


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial


@register.filter
def json(value):
    if isinstance(value, Model):
        value = model_to_dict(value)
    return simplejson.dumps(value, default=json_serial)


ips = ['10.1.50.201', '10.1.50.202', '10.1.50.203',
       '10.1.50.204', '10.1.50.205', '10.1.50.206',
       '10.1.50.207', '10.1.50.208', '10.1.50.209',
       '10.1.50.210', '10.1.50.211', '10.1.50.212']


class Fake:
    pass


def setFanSpeed(fanSpeed):

    # loop through the ips of the servers 
    # maybe we can make the ips modifyable later
    for ip in ips:

        # init the mechanize browser
        br = mechanize.Browser()
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)

        # Browser options - check if these be needed
        br.set_handle_equiv(True)
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)

        # Follows refresh 0 but not hangs on refresh > 0
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # set User-Agent 
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


        # Login to server
        r = br.open('http://' + ip + '/')
        html = r.read()
        br.select_form(nr=0)
        br.form['name'] = 'ADMIN'
        br.form['pwd'] = 'ADMIN'
        br.submit()


        # Follow the redirect to the main page
        # may not be entirely necessary
        x = Fake()
        x.absolute_url = "http://" + ip + "/cgi/url_redirect.cgi?url_name=mainmenu"

        br.follow_link(x)

        # max speed is 1
        # optimal speed is 2
        data = urllib.urlencode({'FanMode':fanSpeed,'smartcool':'0'})

        r = br.open("http://" + ip + "cgi/config_fan_mode.cgi", data)

        print r.read()
