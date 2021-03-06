from .__init__ import *
from .Utils import *
from .Miner import Miner
from .Block import Block

DEBUG_ENABLE = False

class BlockChain(object):

	def __init__(self,difficulty=5):
		self.difficulty = difficulty
		self.chain = [self.createSeedBlock()]

	def getLastBlock(self):
		return self.chain[-1]

	def createSeedBlock(self):
		seedPayload = OrderedDict()

		M = Miner('seed-miner')

		seedBlock = Block(seedPayload,self.difficulty)
		seedBlock.setIndex(0)
		seedBlock.setPrevHash('seed')
		seedBlock = M.mine(seedBlock)

		return seedBlock

	def addBlock(self,block):

		self.initIncomingBlock(block)
		self.chain.append(block)

		if self.isLastBlockValid():
			return True

		self.chain.pop()
		return False

	def isLastBlockValid(self):
		return self.isBlockValid(len(self.chain)-1)

	def isBlockValid(self,block_idx):
		if block_idx == 0:
			return self.chain[block_idx].isBlockValid()
		if self.chain[block_idx].data['prevhash'] != self.chain[block_idx-1].calculateHash():
			return False
		if not self.chain[block_idx].isBlockValid() :
			return False
		return True

	def isChainValid(self):
		chainLen = len(self.chain)

		ret = True

		for i in range(chainLen):
			if not self.isBlockValid(i):
				debug_print('Issue at {}->{}'.format(i-1,i))
				ret = False
				pass
		return ret

	def initIncomingBlock(self,block):
		lastBlock = self.getLastBlock()
		block.setIndex(len(self.chain))
		block.setPrevHash(lastBlock.getHash())

if __name__ == '__main__':
	pass