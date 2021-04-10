import json
from flask import Flask, request, jsonify
from flask_graphql import GraphQLView
import threading


from LedgerPackage.LedgerManager import LedgerManager
from LedgerPackage.Transaction import Transaction
from BlockChainPackage.Miner import Miner
from BlockChainPackage.Block import Block
from BlockChainPackage.schema import schema


import DataBase
import os


flask_app = Flask(__name__)

if not flask_app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    print('Cleaning Db ...')
    DataBase.cleanDb()
    print('Init Db ...')
    DataBase.globalDbInit()

from BlockChainPackage.schema import schema


def mongo_to_obj(j):
    return json.dumps(j.to_json())

class Server():
    POOL_TIME = 1  # seconds
    UPDATE_TIME = 10

    def __init__(self):

        self.LM = LedgerManager('LM')
        self.LM_lock = threading.Lock()
        self.updateThread = None
        self.app = flask_app

        self.updateContinuous()

        @self.app.route('/api', methods=['GET'])
        def api():
            return {
                'title': 'Flask React Application',
            }

        @self.app.route('/receive_transactions', methods=['POST'])
        def receive_transactions():
            data = request.data
            self.queueWork(self.addData, [data])
            return 'OK'

        @self.app.route('/show_data', methods=['GET'])
        def show_data():
            return jsonify({
                'ledgerInfo': mongo_to_obj(Block.objects()),
                'pendingTransactions': [mongo_to_obj(t) for t in self.LM.pendingTransactions],
                'pendingLedgers': [mongo_to_obj(b) for b in self.LM.pendingLedgers]
            })

        self.app.add_url_rule("/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True))

    def update(self):
        self.LM.generatePendingLedgers()
        M = Miner('Teja')
        minable_block = self.LM.getLastestLedgerToMine()

        if minable_block:
            print('Started Mining')
            mined_block = M.mine(minable_block)
            self.LM.authenticateLedger(M,mined_block)
            print('Done Mining')

    def updateContinuous(self):
        self.update()
        self.updateThread = self.queueWork(
            self.updateContinuous, [], workTime=self.UPDATE_TIME)

    def queueWork(self, work, args, workTime=None):
        if not workTime:
            workTime = self.POOL_TIME
        thread = threading.Timer(workTime, work, args=args)
        thread.start()
        return thread

    def addData(self, data):
        with self.LM_lock:
            data = json.loads(data)
            print('Transaction Incomming Data:', data)
            new_t = Transaction()
            new_t.sender = data['From']
            new_t.reciever = data['To']
            new_t.amt = int(data['Amt'])
            self.LM.addTransactionToQueue(new_t)
        return 0


SM = Server()
