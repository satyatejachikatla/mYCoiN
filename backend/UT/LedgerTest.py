import sys
import random
sys.path.append('../')

import DataBase

from LedgerPackage.LedgerManager import LedgerManager
from LedgerPackage.Transaction import Transaction
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

def testBasicLedgering():
    '''testBasicLedgering'''
    LM = LedgerManager('LM')

    for i in range(95):
        f = str(random.randint(0,100))
        t = str(random.randint(0,100))
        amt = random.randint(0,1000)

        trnsct = Transaction()
        trnsct.sender = f
        trnsct.reciever = t
        trnsct.amt = amt

        LM.addTransactionToQueue(trnsct)

    LM.generatePendingLedgers()

    M = Miner('Teja')
    minable_block = LM.getLastestLedgerToMine()
    assert(minable_block != None)

    mined_block = M.mine(minable_block)

    assert(mined_block != None)


    assert(LM.authenticateLedger(M,mined_block))

    print_json(Block.objects().to_json())
    print('Validity:',LM.isLedgerValid())
    print_json(LM.pendingTransactions[-1].to_json())


tests_list = [
    testBasicLedgering,
]

if __name__ == '__main__':
    for i,test in enumerate(tests_list):
        print('----------Test({})----------'.format(i))
        print('DESCRIPTION: {}'.format(test.__doc__))
        test()
        print('----------------------------')

