from .__init__ import *
from .Utils import *

class Block(object):
	def __init__(self,payload,difficulty):
		self.data = OrderedDict()

		self.data['payload'] = payload
		self.data['difficulty'] = difficulty
		self.data['nonce'] = 0
		self.data['index'] = None
		self.data['time']=str(time())
		self.data['prevhash'] = None
		
		self.hash = 'NotComputed'

	def setIndex(self,index):
		self.data['index'] = index

	def setPrevHash(self,prevhash):
		self.data['prevhash'] = prevhash

	def getBlockJSON(self):
		return json.dumps(self.data)

	def getHash(self):
		return self.hash

	def getDifficulty(self):
		return self.data['difficulty']

	def calculateHash(self):
		assert(self.data['index'] != None and self.data['prevhash'] != None)
		return calculateHash(self.getBlockJSON())

	def calculateAndSetHash(self):
		self.hash = self.calculateHash()

	def isBlockValid(self):
		'''
		if hash stats with difficulty 
			then accept hash
		Eg:
			difficulty = 3
			hash = 123ac... then accept
		'''
		self.calculateAndSetHash()
		difficultyString = ''.join(list(map(str,list(range(1,self.data['difficulty']+1)))))
		if self.hash.startswith(difficultyString):
			return True
		return False

if __name__ == '__main__':
	pass