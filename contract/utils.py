from web3 import Web3 

import contract
from .models import BlockchainLog
from django.utils.timezone import make_aware
import datetime

def sync_logs_from_blockchain(contract, w3: Web3):
    logs = contract.events.Log().get_logs(from_block=0)

    for log in logs:
        tx_hash = log["transactionHash"].hex()
        block = w3.eth.get_block(log["blockNumber"])
        timestamp = make_aware(datetime.datetime.utcfromtimestamp(block["timestamp"]))

        # Avoid duplicates
        if not BlockchainLog.objects.filter(tx_hash=tx_hash).exists():
            BlockchainLog.objects.create(
                message=log["args"]["message"],
                block_number=log["blockNumber"],
                tx_hash=tx_hash,
                timestamp=timestamp,
            )

def sync_log_by_tx_hash(tx_hash,w3:Web3,contract):
    receipt = w3.eth.get_transaction_receipt(tx_hash)
    logs = contract.events.Log().process_receipt(receipt)

    for log in logs:
        tx_hash = log["transactionHash"].hex()
        block = w3.eth.get_block(log["blockNumber"])
        timestamp = make_aware(datetime.datetime.utcfromtimestamp(block["timestamp"]))

        if not BlockchainLog.objects.filter(tx_hash=tx_hash).exists():
            BlockchainLog.objects.create(
                message=log["args"]["message"],
                block_number=log["blockNumber"],
                tx_hash=tx_hash,
                timestamp=timestamp,
            )            