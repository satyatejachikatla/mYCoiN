from .__init__ import *
from .Transaction import Transaction
from BlockChainPackage.BlockChain import BlockChain
from BlockChainPackage.Block import Block
from BlockChainPackage.Miner import Miner 

class LedgerManager(object):
    def __init__(self,name:str):
        self.name = name
        self.mineReward = 16
        self.difficulty = 3
        self.transactionsBatchSize = 10

        self.pendingTransactions = []
        self.pendingLedgers = []
        self.BC = BlockChain(self.difficulty)

    def addTransactionToQueue(self,transaction:Transaction):
        self.pendingTransactions.append(transaction)

    def getLatestTrasactionBatch(self) -> List[Transaction]:
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

            new_ledger = Block()
            new_ledger.payload = batch
            new_ledger.prevhash = self.BC.getLastBlock().hash
            new_ledger.difficulty = self.difficulty

            self.pendingLedgers.append(new_ledger)
            self.clearLatestTrasactionBatch()

    def getLastestLedgerToMine(self) -> Block:
        if not self.pendingLedgers:
            return None
        return self.pendingLedgers[0]

    def clearLastestLedgerToMine(self):
        if self.pendingLedgers:
            self.pendingLedgers.pop(0)

    def authenticateLedger(self,miner:Miner,new_ledger:Block):

        status = self.BC.addBlock(new_ledger)

        if status:
            self.clearLastestLedgerToMine()

            miner_reward = Transaction()
            miner_reward.sender = self.name
            miner_reward.reciever = miner.name
            miner_reward.amt = self.mineReward

            self.addTransactionToQueue(miner_reward)

        return status

    def isLedgerValid(self):
        return self.BC.isChainValid()

if __name__ == '__main__':
    pass
