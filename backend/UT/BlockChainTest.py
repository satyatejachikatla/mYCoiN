import sys
sys.path.append('../')

from BlockChainPackage.__init__ import *
import DataBase

from BlockChainPackage.BlockChain import BlockChain
from BlockChainPackage.Miner import Miner
from BlockChainPackage.Block import Block
from BlockChainPackage.Utils import calculateHash , print_json

import pprint

pp = pprint.PrettyPrinter(indent=4)

print('Cleaning Db ...')
DataBase.cleanDb()
print('Init Db ...')
DataBase.globalDbInit()

class Payload(mongoengine.EmbeddedDocument):
    a = mongoengine.IntField()
    b = mongoengine.IntField()

def genDummyChain():
    difficulty = 3
    BC = BlockChain(difficulty)
    M = Miner('miner-boiee')

    for i in range(1,3):
        print('Generating Payload ',i)
        payload=Payload()
        payload.a=i
        payload.b=i

        B = Block()
        B.payload = payload
        B.prevhash = BC.getLastBlock().hash
        B.difficulty = difficulty

        B = M.mine(B)
        assert(BC.addBlock(B))

    return BC	

BC = genDummyChain()

def testBasicBlockChain():
    '''testBasicBlockChain'''

    print_json(Block.objects().to_json())
    assert(BC.isChainValid())
    print('Validity:',BC.isChainValid())

def testConsistantHashing():
    '''testConsistantHashing'''
    payloadData= Payload()

    payloadData.a = 12
    payloadData.b = 23

    pp.pprint([payloadData,
               calculateHash(payloadData.to_json()),
               calculateHash(payloadData.to_json()),
               calculateHash(payloadData.to_json()) == calculateHash(payloadData.to_json())])

def testChainBreakage():
    '''testChainBreakage'''
    b= BC.getLastBlock()
    b.prevhash = 'junk'
    b.save_force()

    print_json(Block.objects().to_json())
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

