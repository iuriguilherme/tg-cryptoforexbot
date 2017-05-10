# vim:fileencoding=utf-8
## Standard output debugging

import datetime

class stdout():
	def __init__(self):
		pass
	def debug(self, message):
		now = str(datetime.datetime.now())
		print '[%s] DEBUG: %s' % (now, message)
	def info(self, message):
		now = str(datetime.datetime.now())
		print '[%s] INFO: %s' % (now, message)
	def err(self, message):
		now = str(datetime.datetime.now())
		print '[%s] ERR: %s' % (now, message)
	def cmd(self, command):
		now = str(datetime.datetime.now())
		print '[%s] CMD: Running %s' % (now, command)
	def rcv(self, target, message):
		now = str(datetime.datetime.now())
		print '[%s] RCV: Received "%s" from %s' % (now, message, target)
	def send(self, target, message):
		now = str(datetime.datetime.now())
		print '[%s] SEND: Sending "%s" to %s' % (now, message, target)

