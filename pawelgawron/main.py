from time import time
import hashlib
import json

class Blockchain:
    def __init__(self):
        self.pg_blocks = []
        self.pg_current_transactions = []

    def pg_add_block(self, nonce=60076):
        if len(self.pg_blocks) == 0:
            genesis = {}
            genesis["index"] = 0
            genesis["timestamp"] = time()
            genesis["transactions"] = self.pg_current_transactions
            genesis["nonce"] = nonce
            genesis["previous_hash"] = "Gawron"
            self.pg_blocks.append(genesis)
        else:
            lastBlock = self.pg_blocks[-1]
            newBlock = {}
            newBlock["index"] = len(self.pg_blocks)
            newBlock["timestamp"] = time()
            newBlock["transactions"] = self.pg_current_transactions
            newBlock["nonce"] = nonce
            newBlock["previous_hash"] = self.pg_hash(lastBlock)
            self.pg_blocks.append(newBlock)

        self.pg_current_transactions = []

    def pg_hash(self, lastBlock):
        lastBlock_string = json.dumps(lastBlock, sort_keys=True)
        lastBlock_encoded = lastBlock_string.encode()
        return hashlib.sha256(lastBlock_encoded).hexdigest()