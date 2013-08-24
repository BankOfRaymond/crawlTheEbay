import requests
import json
'''
class listing
holds a listing from API call to JSON

ebay_item_id INT PRIMARY KEY,
title VARCHAR(255),
category_id INT,
gallery_url_id INT,
view_item_url VARCHAR(255),
product_id INT,
postal_code INT,
location VARCHAR(30),
country_id INT,
currency_id INT,
current_price BIGINT,
bid_count INT,
sold TINYINT,
best_offer_enabled TINYINT,
buy_it_now_available TINYINT,
start_time DATETIME,
end_time DATETIME,
listing_type VARCHAR(12),
is_gift TINYINT,
condition_state_id INT,
is_multivariation_listing TINYINT,
year INT,
miles INT,
top_rated_listing TINYINT
'''

class Listing():
	# ebay_item_id			= None
	# title					= None
	# category_id				= None
	# gallery_url 			= None	#LIST
	# view_item_url			= None	#LIST
	# #product_id				= None
	# postal_code				= None
	# location				= None
	# country_id				= None
	# currency_id				= None
	# current_price			= None
	# bid_count				= None
	# sold					= None
	# best_offer_enabled		= None
	# buy_it_now_available	= None
	# start_time				= None
	# end_time				= None
	# listing_type			= None
	# is_gift					= None
	# condition_state_id		= None
	# is_multivariation_listing	= None
	# year					= None
	# miles					= None
	# top_rated_listing		= None
		# self.ebay_item_id 	= item['itemId'][0].encode("utf-8")
		
		# self.title 			= item['title'][0].encode("utf-8")
		# self.category_id	= item['primaryCategory'][0]['categoryId'][0].encode("utf-8")
		# self.gallery_url 	= [link.encode("utf-8") for link in item['galleryURL']]
		# self.view_item_url  = [link.encode("utf-8") for link in item['viewItemURL']]
		# #self.product_id 	= 
		# self.postal_code 	= item['postalCode'][0].encode("utf-8")
		# self.location		= item['location'][0].encode("utf-8")
		# self.country_id		= item['country']


	listObj	= None

	def __init__(self,item):
		self.listObj = item

	def setVar():
		True









response = requests.get("http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findCompletedItems&SERVICE-VERSION=1.7.0&SECURITY-APPNAME=CyranoIn-611f-4171-9fa9-f5abeff8353d&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&GLOBAL-ID=EBAY-MOTOR&categoryId=6001&sortOrder=EndTimeSoonest&itemFilter(0).name=SoldItemsOnly&itemFilter(0).value=true&paginationInput.entriesPerPage=1").json()

sampleJson = response["findCompletedItemsResponse"][0]['searchResult'][0]['item'][0]

