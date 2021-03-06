from .__init__ import *
from .Transaction import Transaction
from BlockChainPackage.BlockChain import BlockChain
from BlockChainPackage.Block import Block

class LedgerManager(object):
	def __init__(self,name):
		self.name = name
		self.mineReward = 16
		self.difficulty = 3
		self.transactionsBatchSize = 10

		self.pendingTransactions = []
		self.pendingLedgers = []
		self.BC = BlockChain(self.difficulty)

	def addTransactionToQueue(self,transaction):
		self.pendingTransactions.append(transaction)

	def getLatestTrasactionBatch(self):
		if len(self.pendingTransactions) < self.transactionsBatchSize:
			#print('Still need to fill up minimum number of transactions per block for batch {}'.format(self.pendingTransactions))
			return []
		return self.pendingTransactions[:self.transactionsBatchSize]

	def clearLatestTrasactionBatch(self):
		self.pendingTransactions = self.pendingTransactions[self.transactionsBatchSize:]

	def generatePendingLedgers(self):
		while True:
			batch = self.getLatestTrasactionBatch()
			if not batch:
				break

			payload = OrderedDict()
			payload['TransactionData'] = [ transaction.getData() for transaction in batch ]

			new_ledger = Block(payload,self.BC.difficulty)

			self.pendingLedgers.append(new_ledger)

			self.clearLatestTrasactionBatch()

	def getLastestLedgerToMine(self):
		if not self.pendingLedgers:
			return None
		self.BC.initIncomingBlock(self.pendingLedgers[0])
		return self.pendingLedgers[0]

	def clearLastestLedgerToMine(self):
		if self.pendingLedgers:
			self.pendingLedgers.pop(0)
		
	def authenticateLedger(self,miner):
		new_ledger = miner.getMinedBlock()

		status = self.BC.addBlock(new_ledger)

		if status:
			self.clearLastestLedgerToMine()

		self.addTransactionToQueue(Transaction(self.name,miner.name,self.mineReward))

		return status
		

	def isLedgerValid(self):
		return self.BC.isChainValid()

if __name__ == '__main__':
	pass