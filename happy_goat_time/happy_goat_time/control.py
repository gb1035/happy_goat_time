#! /usr/bin/env python

# http://stockrt.github.io/p/emulating-a-browser-in-python-with-mechanize/

import mechanize
import cookielib
import urllib
import threading
import sys
import argparse

ips = ['10.1.50.201', '10.1.50.202', '10.1.50.203',
       '10.1.50.204', '10.1.50.205', '10.1.50.206',
       '10.1.50.207', '10.1.50.208', '10.1.50.209',
       '10.1.50.210', '10.1.50.211', '10.1.50.212']


class Fanmageddon(threading.Thread):

	def __init__(self, ip, fanSpeed):
		super(Fanmageddon, self).__init__()
		self.address = ip
		self.fanSpeed = fanSpeed

	def run(self):
		self.setFanSpeed(str(self.fanSpeed))

	def setFanSpeed(self, fanSpeed):

	    # loop through the ips of the servers 
	    # maybe we can make the ips modifyable later

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
			r = br.open('http://' + self.address + '/')
			html = r.read()
			br.select_form(nr=0)
			br.form['name'] = 'ADMIN'
			br.form['pwd'] = 'ADMIN'
			br.submit()



			# make the post to change fan speed
			data = urllib.urlencode({'FanMode':fanSpeed,'smartcool':'0'})

			r = br.open("http://" + self.address + "/cgi/config_fan_mode.cgi", data)

			print "host " + self.address + " is: " + r.read()
		except:
			print "host " + self.address + " offline"

# Show args
parser = argparse.ArgumentParser()
parser.add_argument('--speed', help='--speed <1|2>')
parser.add_argument('--max', action='store_true', help='turn fans on max speed')
parser.add_argument('--reg', action='store_true', help='turn fans on regular speed')
args = parser.parse_args()



if __name__ == '__main__':
	# this no work atm
	if args.speed is None and args.max is None and args.reg is None:
		parser.print_help()
		exit(0)
	for ip in ips:
		if args.speed == "1" or args.speed == "2":
			x = Fanmageddon(ip, args.speed)
			x.start()
		elif args.max:
			x = Fanmageddon(ip, "1")
			x.start()
		elif args.reg:
			x = Fanmageddon(ip, "2")
			x.start()


