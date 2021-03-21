import json
from flask import Flask, request, jsonify
import threading


from LedgerPackage.LedgerManager import LedgerManager
from LedgerPackage.Transaction import Transaction
from BlockChainPackage.Miner import Miner

flask_app = Flask(__name__)


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
                'ledgerInfo': [{'data': block.data, 'hash': block.hash} for block in self.LM.BC.chain],
                'pendingTransactions': [t.data for t in self.LM.pendingTransactions],
                'pendingLedgers': [b.data for b in self.LM.pendingLedgers]
            })

    def update(self):
        self.LM.generatePendingLedgers()

    def updateContinuous(self):
        self.update()
        self.updateThread = self.queueWork(
            self.updateContinuous, [], workTime=self.UPDATE_TIME)

    def queueWork(self, work, args, workTime=None):
        if not workTime:
            workTime = self.POOL_TIME
        thread = threading.Timer(workTime, work, args=args)
        thread.start()

    def addData(self, data):
        with self.LM_lock:
            data = json.loads(data)
            print('Transaction Incomming Data:', data)
            self.LM.addTransactionToQueue(
                Transaction(data['From'], data['To'], data['Amt']))
        return 0


SM = Server()
