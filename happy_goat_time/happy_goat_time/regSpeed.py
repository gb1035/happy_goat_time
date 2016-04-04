# http://stockrt.github.io/p/emulating-a-browser-in-python-with-mechanize/

import mechanize
import cookielib
import urllib

ips = ['10.1.50.201', '10.1.50.202', '10.1.50.203',
       '10.1.50.204', '10.1.50.205', '10.1.50.206',
       '10.1.50.207', '10.1.50.208', '10.1.50.209',
       '10.1.50.210', '10.1.50.211', '10.1.50.212']


class Fake:
    pass


def setFanSpeed(fanSpeed):

    # loop through the ips of the servers 
    # maybe we can make the ips modifyable later
    for address in ips:

	try:
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
		r = br.open('http://' + address + '/')
		html = r.read()
		br.select_form(nr=0)
		br.form['name'] = 'ADMIN'
		br.form['pwd'] = 'ADMIN'
		br.submit()


		# Follow the redirect to the main page
		# may not be entirely necessary
		x = Fake()
		x.absolute_url = "http://" + address + "/cgi/url_redirect.cgi?url_name=mainmenu"

		br.follow_link(x)

		# max speed is 1
		# optimal speed is 2
		data = urllib.urlencode({'FanMode':fanSpeed,'smartcool':'0'})

		r = br.open("http://" + address + "/cgi/config_fan_mode.cgi", data)

		print r.read()
	except:
		print "host " + address + " offline"

# Set to max speeds
setFanSpeed('2')


