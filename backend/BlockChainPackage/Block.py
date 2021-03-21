from .__init__ import *
from .Utils import *

class Block(mongoengine.DynamicDocument):
    difficulty = mongoengine.IntField(required=True)
    index = mongoengine.IntField(default=lambda : 0)
    nonce = mongoengine.IntField(default=lambda : 0)
    time = mongoengine.DateTimeField(required=True,default=datetime.datetime.now)

    prevhash = mongoengine.StringField(default=lambda:'')
    hash = mongoengine.StringField(default=lambda:'')

    meta = {
        'db_alias': DataBase.dbConfig['alias'],
        'collection': 'Blocks'
    }

    def save(self, *args, **kwargs):
        assert(Block.objects().filter(hash=self.prevhash) or self.index == 0)
        assert(self.isBlockValid())
        super(Block, self).save(*args, **kwargs)

    def save_force(self, *args, **kwargs):
        super(Block, self).save(*args, **kwargs)


    def calculateHash(self):
        assert(self.prevhash != None)

        data = json.loads(self.to_json())
        data_keys = set(data.keys())

        for key in data_keys:
            if key not in ('prevhash','payload','nonce'):
                data.pop(key)

        self.hash = calculateHash(json.dumps(data,indent=4,sort_keys=True))

    def isBlockValid(self) -> bool:
        '''
        if hash stats with difficulty 
                then accept hash
        Eg:
                difficulty = 3
                hash = 123ac... then accept
        '''

        self.calculateHash()
        validity= True
        if self.index != 0:
            validity = Block.objects().filter(hash=self.prevhash) and True

        difficultyString = ''.join(
            list(map(str, list(range(1, self.difficulty+1)))))
        if not self.hash.startswith(difficultyString):
            validity = False
        return validity




if __name__ == '__main__':
    pass
