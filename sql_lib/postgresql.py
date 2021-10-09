import psycopg2 as pgsql



class database:

	def __init__(self, db_name, user, password, host):
		self.db_name = db_name
		self.user = user
		self.passwd = password
		self.host = host
		self.conn = None
		self.curr = None
	def connect(self):
		"""

		"""
		conn = pgsql.connect(dbname=self.db_name, user=self.user, 
								password=self.passwd, host=self.host)
		cursor = conn.cursor()
		self.conn = conn
		self.curr = cursor
		return (conn, cursor)

	def getUserData(self, user_id):
		pass

	def writeUserData(self, user_id, service, password):
		pass