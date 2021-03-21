from .__init__ import *
from .Utils import *
from .Miner import Miner
from .Block import Block

class DummyPayload(mongoengine.EmbeddedDocument):
    time = mongoengine.DateTimeField(required=True,default=datetime.datetime.now)

class BlockChain(object):

    def __init__(self, difficulty:int = 3):
        self.difficulty = difficulty
        self.__createSeedBlock()

    def __createSeedBlock(self):
        if self.getLastBlock():
            return

        M = Miner('seed-miner')

        seedBlock = Block()
        seedBlock.payload = DummyPayload()
        seedBlock.prevhash = 'seed'
        seedBlock.difficulty = self.difficulty

        seedBlock = M.mine(seedBlock)

        seedBlock.save()

    def getLastBlock(self) -> Block:
        lastBlock = Block.objects().order_by('-_id').first()
        return lastBlock

    def addBlock(self, block:Block) -> bool:
        block.index = self.getLastBlock().index + 1
        block.difficulty = self.difficulty
        if block.isBlockValid():
            block.save()
            return True
        return False

    def isChainValid(self) -> bool:
        query = Block.objects()
        for block in query:
            if not block.isBlockValid():
                return False
        return True

if __name__ == '__main__':
    pass
