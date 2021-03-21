from .__init__ import *
import json

class Transaction(mongoengine.EmbeddedDocument):
    sender = mongoengine.StringField(required=True)
    reciever = mongoengine.StringField(required=True)
    amt = mongoengine.FloatField(required=True)

    time = mongoengine.DateTimeField(required=True,default=datetime.datetime.now)

if __name__ == '__main__':
    pass
