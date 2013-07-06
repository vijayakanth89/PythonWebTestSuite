from sqlite3 import dbapi2 as sqlite
from time import time
from datetime import datetime

class SqliteHelper:
	
	def __init__(self):
		self.conn = sqlite.connect('/tmp/test', check_same_thread=False)
		self.cursor = self.conn.cursor()

	def create_tables(self):
		self.cursor.execute("create table log (app_id text, time timestamp, type text, message text)")
		self.conn.commit()

	def insert(self, app_id, t, message):
		self.cursor.execute("insert into log(app_id, time, type, message) values(?,?,?,?)", \
					   	(app_id, time(), t, message))
		self.conn.commit()

	def close(self):
		self.cursor.close()

		
if __name__ == '__main__':
	db = SqliteHelper()
	db.create_tables()
	db.close()
