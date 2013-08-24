

import requests
import json

url = "http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findCompletedItems&SERVICE-VERSION=1.7.0&SECURITY-APPNAME=CyranoIn-611f-4171-9fa9-f5abeff8353d&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&GLOBAL-ID=EBAY-MOTOR&categoryId=31874&sortOrder=EndTimeSoonest&paginationInput.entriesPerPage=1"


# try:
response = requests.get(url)


# except urllib2.URLError, e:
# 	handleError(e)
# 	result = 'Nothing'

t = response.json()