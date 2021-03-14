from .__init__ import *
from .Utils import *
from .Block import Block

class Miner(object):
	def __init__(self,name):
		self.name = name
		self.minedBlock = None

	def setMinedBlock(self,block):
		self.minedBlock = block

	def getMinedBlock(self):
		return self.minedBlock

	def mine(self,block):
		ret = None
		skip = 0
		skip_amount = 100
		while ret == None:
			r = range(0+skip,skip_amount+skip)
			ret = self.mine_range(block,r)
			skip += skip_amount

		return ret

	def mine_range(self,block,r):
		return self.mine_set(block,list(r))

	def mine_set(self,block,nonce_set):
		'''
		if hash stats with difficulty 
			then accept hash
		else
			nonce + 1 and repeat
		Eg:
			difficulty = 3
			hash = 123ac... then accept
		'''
		block.calculateAndSetHash()

		for nonce in nonce_set:
			block.data['nonce'] = nonce
			if block.isBlockValid():
				debug_print('Found : Hash : {hash}\nNonce: {nonce}'.format(hash=block.hash,nonce=block.data['nonce']))
				return block

			debug_print('Mining : Curr Hash : {hash}\nNonce: {nonce}'.format(hash=block.hash,nonce=block.data['nonce'] ))

		debug_print('Not Found')
		return None

if __name__ == '__main__':
	pass