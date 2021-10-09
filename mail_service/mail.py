import secrets 

from websocket import create_connection
import sys
from json import loads
from subprocess import call
from datetime import datetime

class mailbox(object):
	"""10 minute mailbox"""
	def __init__(self):
		super(mailbox, self).__init__()
		self.websocket = create_connection("wss://dropmail.me/websocket")
		self.next = self.ws.recv
		self.close_ws = self.ws.close
		self.email = self.next()[1:].split(":")[0]
		self.next()

def main(box):
	while True:
		result =  box.next()
		try:
			print(f"Recieved following at {datetime.now()}")
			for k in loads(result[1:]).items():
				print("\t%s: %s" % k)
		except:
			print(f"Recieved:{datetime.now()} {result}\n")

if __name__ == '__main__':
	import os
	print("PID: {0}\nIf you can't quite, run 'kill {0}'\n".format(os.getpid()))
	try:
		box = mailbox()
		main(box)
	except KeyboardInterrupt:
		box.close()
		sys.exit(0)

