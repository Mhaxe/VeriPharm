# blockchain/eth_utils.py
from web3 import Web3
import json
import os

# Load ABI and contract address (update paths as needed)
with open("contract/VeripharmABI.json") as f:
    abi = json.load(f)

contract_address = "0xYourDeployedContractAddress"

# Connect to Hardhat local node
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
contract = w3.eth.contract(address=contract_address, abi=abi)

def get_contract_instance():
    return contract
