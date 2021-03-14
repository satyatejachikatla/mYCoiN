from .__init__ import *
import json

class Transaction(object):
	def __init__(self,sender,reciever,amt):
		self.data = OrderedDict()

		self.data['sender'] = sender
		self.data['reciever'] = reciever
		self.data['amt'] = amt
		self.data['time'] = str(time())

	def getData(self):
		return self.data


if __name__ == '__main__':
	pass