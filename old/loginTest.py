# import requests
# import sys


USER = 'spoontherocket821'
PASSWORD = 'Supermanfly'
url = "http://www.ebay.com"
import mechanize
import cookielib
import time

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


time.sleep(1)

# br.open(url)
# req = br.click_link(text="Sign in")
# br.open(req)
# br.select_form(nr=1)
# br.form['userid'] 	= USER
# br.form['pass']		= PASSWORD

# time.sleep(1)

# br.submit()
# #browser doesn't redirect need to click continue to get to "My ebay page"
# req = br.click_link(text="Continue")
# r = br.open(req)
# loggedIn = r.read()
# print loggedIn

# get to home page 
#br.click_link(text='eBayeBay[IMG]')

