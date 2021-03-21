from .__init__ import *
from .Utils import *
from .Block import Block

class Miner(object):
    def __init__(self,name:str):
        self.name = name

    def mine(self,block:Block)->Block:
        ret = None
        skip = 0
        skip_amount = 100
        while ret == None:
            r = range(0+skip,skip_amount+skip)
            ret = self.mine_range(block,r)
            skip += skip_amount

        return ret

    def mine_range(self,block:Block,r:range) -> Block:
        return self.mine_set(block,set(r))

    def mine_set(self,block:Block,nonce_set:set) -> Block:
        '''
        if hash stats with difficulty 
                then accept hash
        else
                nonce + 1 and repeat
        Eg:
                difficulty = 3
                hash = 123ac... then accept
        '''

        for nonce in nonce_set:
            block.nonce = nonce
            if block.isBlockValid():
                debug_print(f'Found : Hash : {block.hash}\nNonce: {block.nonce}')
                return block

            debug_print(f'Mining : Hash : {block.hash}\nNonce: {block.nonce}')

        debug_print('Not Found')
        return None

if __name__ == '__main__':
    pass
