import json
from flask import Flask, request, jsonify
import threading


from LedgerPackage.LedgerManager import LedgerManager
from LedgerPackage.Transaction import Transaction
from BlockChainPackage.Miner import Miner

flask_app = Flask(__name__)


class StateMachine():
    POOL_TIME = 1  # seconds

    def __init__(self):

        self.LM = LedgerManager('LM')
        self.LM_lock = threading.Lock()

        self.state_thread = threading.Thread()

        self.app = flask_app

        @self.app.route('/api', methods=['GET'])
        def api():
            return {
                'userId': 1,
                'title': 'Flask React Application',
                'compleated': False
            }

        @self.app.route('/receive_transactions', methods=['POST'])
        def receive_transactions():
            self.data = request.data
            self.queueWork(self.addData)
            return 'OK'

        @ self.app.route('/show_ledger', methods=['GET'])
        def show_ledger():
            return jsonify([{'data': block.data, 'hash': block.hash} for block in self.LM.BC.chain])

        @ self.app.route('/update', methods=['GET'])
        def update():

            print(self.LM.pendingTransactions)

            self.LM.generatePendingLedgers()

            M = Miner('Teja')
            minable_block = self.LM.getLastestLedgerToMine()

            if minable_block:
                mined_block = M.mine(minable_block)
                M.setMinedBlock(mined_block)
                self.LM.authenticateLedger(M)
                return 'DONE'
            return 'SKIPPED'

    def queueWork(self, work):
        thread = threading.Timer(self.POOL_TIME, work, ())
        thread.start()

    def addData(self):
        with self.LM_lock:
            data = json.loads(self.data)
            print(data)
            self.LM.addTransactionToQueue(
                Transaction(data['From'], data['To'], data['Amt']))
        return 0


SM = StateMachine()
