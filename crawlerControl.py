'''
Instantiates the crawler 

Crawler has list of categories to crawl
begins crawl loop
	for each crawl instantiate new Database Controller
	load into Database
	close Database

'''
import dbControl
import requests
import time
import datetime

class APICall():
	url							= None
	OPERATIONNAME				= None
	SERVICEVERSION				= None
	SECURITYAPPNAME				= None
	RESPONSEDATAFORMAT			= None
	RESTPAYLOAD 				= None
	GLOBALID					= None
	categoryId					= None
	sortOrder					= None
	itemFilter0name				= None
	itemFilter0value			= None
	paginationInputentriesPerPage = None
	paginationInputpageNum		= None

	def __init__(self,catID,pageNum):
		self.OPERATIONNAME 			="findCompletedItems"
		self.SERVICEVERSION 		="1.7.0"
		self.SECURITYAPPNAME		="CyranoIn-611f-4171-9fa9-f5abeff8353d"
		self.RESPONSEDATAFORMAT		="JSON"
		self.RESTPAYLOAD			=''
		self.GLOBALID 				="EBAY-MOTOR"
		self.categoryId 			= str(catID)
		self.sortOrder 				="EndTimeSoonest"
		self.itemFilter0name 		="SoldItemsOnly"
		self.itemFilter0value 		="true"
		self.paginationInputentriesPerPage="100"
		self.paginationInputpageNumber  = str(pageNum)

	def getAPICall(self):
		return "".join(("http://svcs.ebay.com/services/search/FindingService/v1?",\
						"OPERATION-NAME=",	self.OPERATIONNAME,"&"\
						"SERVICE-VERSION=",	self.SERVICEVERSION,"&"\
						"SECURITY-APPNAME=",self.SECURITYAPPNAME,"&"\
						"RESPONSE-DATA-FORMAT=",self.RESPONSEDATAFORMAT,"&"\
						"REST-PAYLOAD","&"\
						"GLOBAL-ID=",		self.GLOBALID,"&"\
						"categoryId=",		self.categoryId,"&"\
						"sortOrder=",		self.sortOrder,"&"\
						"itemFilter(0).name=", self.itemFilter0name,"&"\
						"itemFilter(0).value=", self.itemFilter0value,"&"\
						"paginationInput.entriesPerPage=", self.paginationInputentriesPerPage,"&"\
						"paginationInput.pageNumber=", self.paginationInputpageNumber \
						))

class CrawlerControl():
	dbObj 			= None
	catList 		= None
	crawlCount 		= None
	maxCrawlPerDay 	= None

	def __init__(self):
		self.catList = []
		self.crawlCount = 0
		self.dbObj = dbControl.DBControl()
		self.maxCrawlPerDay = 5000 


	def getListToCrawl(self):
		# self.dbObj.connect()
		# self.dbObj.disconnect()
		# If database empty, then use category 6001
		self.catList.append(6001)
		self.catList.append(6024)
		
	
	def crawl(self):
		for cat in self.catList:
			if self.crawlCount < self.maxCrawlPerDay:
				self.crawlCategory(cat)

	def crawlCategory(self,categoryId):
		firstAPICall = APICall(categoryId,1)
		response = requests.get(firstAPICall.getAPICall()).json()
		
		totalPages = int(response['findCompletedItemsResponse'][0]['paginationOutput'][0]['totalPages'][0])
		self.dbObj.connect()	#DB Connect

		i=1
		while i <= totalPages and self.crawlCount < self.maxCrawlPerDay:# and i <= 100:
			a = APICall(categoryId,i)
			response = requests.get(a.getAPICall()).json()
			self.crawlCount += 1
			print "Category: ",categoryId, "OnPage: ",i, "APICalls: ",self.crawlCount, "Total Pages: ",totalPages
			if "Failure" in response["findCompletedItemsResponse"][0]['ack']:
				time.sleep(15)
				print "Sleeping HTTP response failed"
			else:
				self.insertIntoDB(response)  #Actual call to DB
				time.sleep(1)
				i = i+1
			
		self.dbObj.disconnect()	#DB Disconnect



		#def isInDB(self,table, inColumn, outColumn, data):
		#Ebay specific structure of JSon Response
	def insertIntoDB(self,jRes):
		listing = jRes['findCompletedItemsResponse'][0]['searchResult'][0]['item']

		for l in listing:
			itemID = int(l['itemId'][0])
			#print "ITEM. ",itemID,l['title'][0][:40].encode("utf-8")

			inDB = self.dbObj.isInDB("listing","ebay_item_id","ebay_item_id",itemID)
			#print "In DB: ",inDB

			if inDB is False:

				insertVal = {}
				insertVal["ebay_item_id"] = itemID
				#title
				insertVal['title'] = l['title'][0].encode("utf-8")

				#category_id
				catID = l['primaryCategory'][0]["categoryId"][0].encode("utf-8")
				catInDB = self.dbObj.isInDB("category", "category_id", "category_id", catID)
				if catInDB == False:
					make = l['title'][0].encode("utf-8")
					make = make[:make.find(":")-1]
					self.dbObj.insert("category", ["category_id","model", "make"], [ catID,l['primaryCategory'][0]["categoryName"][0].encode("utf-8"), make ],  )
				insertVal["category_id"] = catID

				#Gallery URL
				if 'galleryPlusPictureURL' in l:
					insertVal["gallery_url"] = l['galleryPlusPictureURL'][0].encode("utf-8")
				elif 'galleryURL' in l:
					insertVal["gallery_url"] = l['galleryURL'][0].encode("utf-8")
				else:
					insertVal["gallery_url"] = ''

				#"view_item_url"
				if 'viewItemURL' in l:	insertVal["view_item_url"] = l['viewItemURL'][0].encode("utf-8")

				# "product_id" Skipping as EBAY motors does not contain product IDS

				# "postal_code" ,\
				if "postalCode" in l:	insertVal['postal_code'] = l['postalCode'][0].encode("utf-8")
				
				#"location" 
				if "location" in l:	insertVal["location"] = l['location'][0].encode("utf-8")
				
				# "country_id" ,\
				if "country" in l:	insertVal["country"] = l['country'][0].encode("utf-8")


				if "sellingStatus" in l:
					if "currentPrice" in l['sellingStatus'][0]:
						insertVal['listing_currency'] 			= l['sellingStatus'][0]['currentPrice'][0]["@currencyId"].encode("utf-8")
						insertVal['listing_currency_price'] 	= l['sellingStatus'][0]['currentPrice'][0]["__value__"].encode("utf-8")
					if "convertedCurrentPrice" in l['sellingStatus'][0]:
						insertVal['converted_currency'] 		= l['sellingStatus'][0]['convertedCurrentPrice'][0]["@currencyId"].encode("utf-8")
						insertVal['converted_currency_price'] 	= l['sellingStatus'][0]['convertedCurrentPrice'][0]["__value__"].encode("utf-8")
					if "bidCount" in l['sellingStatus'][0]:	
						insertVal["bid_count"] 	= l['sellingStatus'][0]['bidCount'][0].encode("utf-8")
					if "sellingState" in l['sellingStatus'][0]:
						insertVal["selling_state"] = l['sellingStatus'][0]['sellingState'][0].encode("utf-8")

				if "listingInfo" in l:
					if "bestOfferEnabled" in l["listingInfo"][0]:
						if l["listingInfo"][0]["bestOfferEnabled"][0].encode("utf-8") == True:
							insertVal["best_offer_enabled"] = 1
						else:	insertVal["best_offer_enabled"] = 0 
					if "buyItNowAvailable" in l["listingInfo"][0]:
						if l["listingInfo"][0]["buyItNowAvailable"][0].encode("utf-8") == True:
							insertVal["buy_it_now_available"] = 1
						else:	insertVal["buy_it_now_available"] = 0 
					if "startTime" in l["listingInfo"][0]:
						a = l["listingInfo"][0]["startTime"][0]
						insertVal["start_time"] = str(a[:10] + " " + a[11:-5])
					if "endTime" in l["listingInfo"][0]:
						a = l["listingInfo"][0]["endTime"][0]
						insertVal["end_time"] = str(a[:10] + " " + a[11:-5])
					if "listingType" in l['listingInfo'][0]:
						insertVal["listing_type"] = l['listingInfo'][0]['listingType'][0].encode("utf-8")

				if "isMultiVariationListing" in l:
					if l["isMultiVariationListing"][0].encode("utf-8") == "true":	insertVal['is_multivariation_listing'] = 1
					else:	insertVal['is_multivariation_listing'] = 0

				# "condition_state_id" ,\
				if "condition" in l:
					condID = l['condition'][0]["conditionId"][0].encode("utf-8")
					conInDB = self.dbObj.isInDB("condition_state", "condition_state_id", "condition_state_id", condID)
					if conInDB == False:
						name = l['condition'][0]["conditionDisplayName"][0].encode("utf-8")
						self.dbObj.insert("condition_state", ["condition_state_id","name"], [ condID,l['condition'][0]["conditionDisplayName"][0].encode("utf-8")]  )
					insertVal["condition_state_id"] = condID
					
					if "attribute" in l:
						for i in range(len(l["attribute"])):
							if "Year" in l["attribute"][i]["name"]:
								insertVal["year"] = l["attribute"][i]["value"][0].encode("utf-8")[:4]
							if "Miles" in l["attribute"][i]["name"]:
								insertVal["miles"] = l["attribute"][i]["value"][0].encode("utf-8")[:4]

				# "top_rated_listing" ]
				if "topRatedListing" in l:
					if l["topRatedListing"][0].encode("utf-8") == "true":	insertVal['top_rated_listing'] = 1
					else:	insertVal['top_rated_listing'] = 0


				columns = []
				data = []
				for item in insertVal:
					columns.append(item)
					data.append(insertVal[item])
				self.dbObj.insert("listing", columns, data)	

				#print insertVal
	
c = CrawlerControl()
c.getListToCrawl()
c.crawl()

