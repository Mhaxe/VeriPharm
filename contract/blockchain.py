from web3 import Web3
import json
import os

# Connect to local or remote Ethereum node
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))  

# Load contract ABI
with open(os.path.join(os.path.dirname(__file__), 'VeripharmABI.json')) as f:
    abi = json.load(f)

contract_address = Web3.to_checksum_address("0x5fbdb2315678afecb367f032d93f642f64180aa3")
contract = w3.eth.contract(address=contract_address, abi=abi)


def log_event(message: str):
    # Replace with appropriate signer and private key management
    account = w3.eth.accounts[0]
    tx = contract.functions.logEvent(message).transact({'from': account})
    receipt = w3.eth.wait_for_transaction_receipt(tx)
    return receipt

def get_contract_instance():
    return contract
