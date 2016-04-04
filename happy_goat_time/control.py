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

fanSpeed = None
maxFan = False
power = False
powerOption = -1
allIps = False

class Fanmageddon(threading.Thread):

	def __init__(self, ip):
		super(Fanmageddon, self).__init__()
		self.address = ip

	def run(self):
		if maxFan:
			self.fanSpeed = fanSpeed
			self.setFanSpeed(str(fanSpeed))
		elif power:
			self.changePower(powerOption)


	def loginToSite(self):
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

			return br
		except:
			print "host " + self.address + " offline"
			return None


	def setFanSpeed(self, fanSpeed):
		try:
			br = self.loginToSite()

			# make the post to change fan speed
			data = urllib.urlencode({'FanMode':fanSpeed,'smartcool':'0'})
			r = br.open("http://" + self.address + "/cgi/config_fan_mode.cgi", data)
			print "host " + self.address + " is: " + r.read()
		except:
			print "host " + self.address + " offline"



	def changePower(self, val):
		# 0 => poweroff imediately
		# 1 => power on
		# 2 => power cycle
		# 3 => reset power
		# 5 => orderly shutdown
		
		try:
			br = self.loginToSite()
			# make the post to reset the machine
			data = urllib.urlencode({'POWER_INFO.XML':'(1,' + str(val) + ')'})
			r = br.open("http://" + self.address + "/cgi/ipmi.cgi", data)
			print "Power should have changed"
		except:
			print "host " + self.address + " unreachable"



	def resetPower(self):
		self.changePower(3)

	def powerOffMeow(self):
		self.changePower(0)

	def powerOffOrderly(self):
		self.changePower(5)

	def powerCycle(self):
		self.changePower(2)

	def powerOn(self):
		self.changePower(1)






# Show args
parser = argparse.ArgumentParser()
parser.add_argument('--ip', action='store', dest='ip', help='specific ip to use')
parser.add_argument('--all', action='store_true', help='run command against all ips')

parser.add_argument('--speed', help='--speed <1|2>')
parser.add_argument('--max', action='store_true', help='turn fans on max speed')
parser.add_argument('--reg', action='store_true', help='turn fans on regular speed')

parser.add_argument('--reset', action='store_true', help='reset a machine')
parser.add_argument('--offMeow', action='store_true', help='power off a machine meow')
parser.add_argument('--turnOn', action='store_true', help='power on a machine')
parser.add_argument('--offOrderly', action='store_true', help='power off the machine orderly')
parser.add_argument('--powerCycle', action='store_true', help='i guess just power cycle the box?')
args = parser.parse_args()



if __name__ == '__main__':
	# # this no work atm
	#if args.speed is None and not args.max and not args.reset and not args.reg:
	#	parser.print_help()
	#	exit(0)

	if args.all:
		# run on all machines
		allIps = True
		for ip in ips:
			if args.speed == "1" or args.speed == "2":
				maxFan = True
				x = Fanmageddon(ip)
				fanSpeed = int(args.speed)
				x.start()

			elif args.max:
				maxFan = True
				x = Fanmageddon(ip)
				fanSpeed = 1
				x.start()

			elif args.reg:
				maxFan = True
				x = Fanmageddon(ip)
				fanSpeed = 2
				x.start()

			elif args.reset:
				power = True
				powerOption = 3
				x = Fanmageddon(ip)
				x.start()

			elif args.offMeow:
				power = True
				powerOption = 0
				x = Fanmageddon(ip)
				x.start()

			elif args.turnOn:
				power = True
				powerOption = 1
				x = Fanmageddon(ip)
				x.start()

			elif args.offOrderly:
				power = True
				powerOption = 5
				x = Fanmageddon(ip)
				x.start()

			elif args.powerCycle:
				power = True
				powerOption = 2
				x = Fanmageddon(ip)
				x.start()


	elif args.ip is not None:

		# only want to do action on single ip
		if args.reset:
			print "Reseting single IP"
			x = Fanmageddon(args.ip)
			x.resetPower()

		elif args.offMeow:
			print "Powering off " + args.ip + " meow"
			x = Fanmageddon(args.ip)
			x.powerOffMeow()

		elif args.turnOn:
			print "Powering on " + args.ip + " meow"
			x = Fanmageddon(args.ip)
			x.powerOn()

		elif args.offOrderly:
			print "Orderly shutting down " + args.ip + " meow"
			x = Fanmageddon(args.ip)
			x.powerOffOrderly()

		elif args.powerCycle:
			print "Power cycling " + args.ip + " meow"
			x = Fanmageddon(args.ip)
			x.powerCycle()


def changeFanSpeed(ips, level):
	for ip in ips:
		if level == 0:
			maxFan = True
			x = Fanmageddon(ip)
			fanSpeed = 1
			x.start()
		elif level == 1:
			maxFan = True
			x = Fanmageddon(ip)
			fanSpeed = 2
			x.start()

def changePower(ips, powerCode):
	# 0 => poweroff imediately
	# 1 => power on
	# 2 => power cycle
	# 3 => reset power
	# 5 => orderly shutdown
	power = True
	powerOption = powerCode
	for ip in ips:
		x = Fanmageddon(ip)
		x.start()


