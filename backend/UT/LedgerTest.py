import sys
import random
sys.path.append('../')

from LedgerPackage.LedgerManager import LedgerManager
from LedgerPackage.Transaction import Transaction
from BlockChainPackage.Miner import Miner

import pprint

pp = pprint.PrettyPrinter(indent=4)


def testBasicLedgering():
	'''testBasicLedgering'''
	LM = LedgerManager('LM')

	for i in range(95):
		f = str(random.randint(0,100))
		t = str(random.randint(0,100))
		amt = random.randint(0,1000)
		LM.addTransactionToQueue(Transaction(f,t,amt))

	LM.generatePendingLedgers()

	M = Miner('Teja')
	minable_block = LM.getLastestLedgerToMine()
	assert(minable_block != None)

	mined_block = M.mine(minable_block)

	assert(mined_block != None)

	M.setMinedBlock(mined_block)

	assert(M.getMinedBlock() != None)

	assert(LM.authenticateLedger(M))

	print('Validity:',LM.isLedgerValid())
	pp.pprint(LM.pendingTransactions[-1].getData())


tests_list = [
	testBasicLedgering,
]

if __name__ == '__main__':
	for i,test in enumerate(tests_list):
		print('----------Test({})----------'.format(i))
		print('DESCRIPTION: {}'.format(test.__doc__))
		test()
		print('----------------------------')
		