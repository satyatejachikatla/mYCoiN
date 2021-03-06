import sys
sys.path.append('../')

from BlockChainPackage.__init__ import *

from BlockChainPackage.BlockChain import BlockChain
from BlockChainPackage.Miner import Miner
from BlockChainPackage.Block import Block
from BlockChainPackage.Utils import calculateHash

import pprint

pp = pprint.PrettyPrinter(indent=4)

def genDummyChain():
	BC = BlockChain(3)
	M = Miner('miner-boiee')

	for i in range(1,6):
		payloadData= OrderedDict({i:i,i+1:i+1})

		B = Block(payloadData,BC.difficulty)

		B.setIndex(i)
		B.setPrevHash(BC.getLastBlock().getHash())

		B = M.mine(B)
		assert(B != None)
		assert(BC.addBlock(B))

	return BC	

def testBasicBlockChain():
	'''testBasicBlockChain'''
	BC = genDummyChain()

	pp.pprint([(block.data,block.hash) for block in BC.chain])
	print('Validity:',BC.isChainValid())

def testConsistantHashing():
	'''testConsistantHashing'''
	payloadData= OrderedDict()

	payloadData['abc'] = 12
	payloadData['efg'] = 23

	pp.pprint([payloadData,
		calculateHash(json.dumps(payloadData)),
		calculateHash(json.dumps(payloadData)),
		calculateHash(json.dumps(payloadData)) == calculateHash(json.dumps(payloadData))])

def testChainBreakage():
	'''testChainBreakage'''
	BC = genDummyChain()

	BC.chain[2].data['payload'] = OrderedDict()
	print('Validity:',BC.isChainValid())


tests_list = [
	testBasicBlockChain,
	testConsistantHashing,
	testChainBreakage
]

if __name__ == '__main__':
	for i,test in enumerate(tests_list):
		print('----------Test({})----------'.format(i))
		print('DESCRIPTION: {}'.format(test.__doc__))
		test()
		print('----------------------------')
		