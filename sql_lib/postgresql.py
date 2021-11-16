#import psycopg2 as pgsql

import sqlite3 as pgsql

class database:

	def __init__(self, db_name="db", user="admin", password="123", host="127.0.0.1"):
		self.db_name = db_name
		self.user = user
		self.passwd = password
		self.host = host
		self.conn = None
		self.curr = None
		self.connect()
	def connect(self):
		"""
		Connects to database with name db_name at host with password
		
		"""
		#conn = pgsql.connect(dbname=self.db_name, user=self.user, password=self.passwd, host=self.host)
		conn = pgsql.connect(self.db_name, check_same_thread=False)
		cursor = conn.cursor()
		self.conn = conn
		self.curr = cursor
		return (conn, cursor)
	def disconnect(self):
		"""
		
		"""
		self.conn.close()
	
	def writeNewUserData(self, user_id, name, surname):
		"""
		Adds new user entry to db

		"""
		sql = "INSERT INTO Users VALUES ((?),(?),(?));"
		res = self.curr.execute(sql, [user_id, name, surname])
		self.conn.commit()

	def getUserData(self, user_id):
		"""
		Get all data about user by id

		"""
		sql = "SELECT * FROM Users WHERE user_id=(?);"
		res = self.curr.execute(sql,[user_id])
		return res.fetchall()
	
	def doesUserExist(self, user_id):
		"""
		Get all data about user by id

		"""
		sql = "SELECT user_id FROM Users WHERE user_id=(?);"
		res = self.curr.execute(sql,[user_id])
		return len(res.fetchall()) > 0

	def writeUserServiceData(self, user_id, service, password):
		"""
		Add new service entry to db for user with id

		"""
		sql = "INSERT INTO Services VALUES ((?),(?),(?));"
		self.curr.execute(sql,[user_id, service, password])
		self.conn.commit()

	def getUserServicePassword(self, user_id, service_name):
		"""
		Get user password for specified service
		
		"""
		sql = "SELECT password FROM Services WHERE user_id=(?) AND service=(?);"
		res = self.curr.execute(sql,[user_id, service_name])
		return res.fetchall()

	def removeUserServicePassword(self, user_id, service_name):
		"""
		Removes specified service password from db
		"""
		sql = "DELETE FROM Services WHERE user_id=(?) AND service=(?);"
		res = self.curr.execute(sql,[user_id, service_name])
		self.conn.commit()
	
	def removeUser(self, user_id):
		"""
		Removes user from db

		"""
		sql = "DELETE FROM Users WHERE user_id=(?);"
		res = self.curr.execute(sql,[user_id])
		return res.fetchall()	
	
	def writeNewMailboxData(self, user_id, mailbox_id, mailbox_name):
		"""
		Adds new mailbox data to db for user_id

		"""
		sql = "INSERT INTO Mailboxes VALUES ((?),(?));"
		self.curr.execute(sql,[user_id, mailbox_id])
		self.conn.commit()

	def getMailboxData(self, user_id):
		"""
		Gets all mailboxes accociated with the user by user_id		
		"""
		sql = "SELECT * FROM Mailboxes WHERE user_id=(?);"
		res = self.curr.execute(sql,[user_id])
		return res.fetchall()

	def removeMailbox(self, user_id, mailbox_id):
		"""
		Removes mailbox from db 
		
		"""
		sql = "DELETE FROM Mailboxes WHERE user_id=(?) and mailbox_id=(?);"
		res = self.curr.execute(sql,[user_id, mailbox_id])
		self.conn.commit()


def main_bad():
	#database = database(r"sql_lib\test_db.db")
	a=1
	i=0
	while a != 0 and i < 10:
		i+=1
		#data = database.getUserData(i)
		data = ("eacdty","qqqeeddttydy")
		for entry in data:
			e_list = []
			for letter in entry:
				if letter == "e":
					e_list.append("a")
				elif letter == "a":
					e_list.append("e")
				elif letter == "c":
					e_list.append("y")
				elif letter == "d":
					e_list.append("t")
				elif letter == "t":
					e_list.append("d")
				elif letter == "y":
					e_list.append("c")
				else: letter=""
			res = "".join(e_list)
			print(res, i)
	#database.disconnect()

def main_good():
	#database = database(r"sql_lib\test_db.db")
	a=1
	i=0
	while a != 0 and i < 10:
		i+=1
		#data = database.getUserData(i)
		data = ("eacdty","qqqeeddttydy")
		repl_array = {"e":"a", "a":"e","c":"y","d":"t","t":"d","y":"c"}
		for entry in data:
			res = "".join([repl_array[letter] for letter in list(entry) if letter in repl_array])
			print(res, i)
				
	#database.disconnect()		
		
if __name__ == "__main__":
	main_good()
	print("________________")
	main_bad()