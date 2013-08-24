import MySQLdb
import credentials

class DBControl():
	USERNAME = None
	PASSWORD = None
	HOST 	 = None
	DATABASE = None

	dbConnection = None

	def __init__(self):
		self.USERNAME 	= credentials.USERNAME
		self.PASSWORD	= credentials.PASSWORD
		self.HOST		= credentials.HOST
		self.DATABASE 	= credentials.DATABASE

	def connect(self):
		self.dbConnection = MySQLdb.connect(self.HOST, self.USERNAME, self.PASSWORD, self.DATABASE)

	def disconnect(self):
		self.dbConnection.close()

	def isInDB(self,table, inColumn, outColumn, data):
		cursor = self.dbConnection.cursor()
		query = "".join(("SELECT ",outColumn," from ", self.DATABASE,".",table, " WHERE ", inColumn, " = '",str(data),"'"))
		cursor.execute(query)
		r = cursor.fetchall()
		if(len(r) < 1):
			return False
		else:
			return r[0]

	def insert(self,table,columns,data):
		query = "INSERT INTO " + self.DATABASE+"."+table + " ( " + ",".join(columns) + " ) " + " VALUES " + "(" +str(data)[1:-1] + ")"
		cursor = self.dbConnection.cursor()
		cursor.execute(query)
		self.dbConnection.commit()


	


	def truncate(self, table):
		cursor = self.dbConnection.cursor()
		query = "".join(("TRUNCATE TABLE ",self.DATABASE,".",table))
		self.dbConnection.commit()
	
	def showAll(self):
		query = "SELECT * from listing;"
		cursor = self.dbConnection.cursor()
		cursor.execute(query)
		print cursor.fetchall()


		query = "SELECT * from category;"
		cursor = self.dbConnection.cursor()
		cursor.execute(query)
		print cursor.fetchall()




# d = DBControl()
# d.connect()
# print d.isInDB("listing","ebay_item_id ", "ebay_item_id","1")
# d.disconnect()