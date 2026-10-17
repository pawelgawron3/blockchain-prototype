from time import time
import hashlib
import json

class Blockchain:
    def __init__(self):
        self.pg_blocks = []
        self.pg_current_transactions = []

    def pg_add_transaction(self, sender, receiver, amount):
        if amount <= 0:
            raise ValueError("The amount of money in transaction has to be greater than 0!")

        transaction = {
            "sender": sender,
            "recipient": receiver,
            "amount": amount
        }

        self.pg_current_transactions.append(transaction)

        return len(self.pg_blocks)

    def pg_add_block(self, nonce=60076):
        if len(self.pg_blocks) == 0:
            block = {
                "index": 0,
                "timestamp": time(),
                "transactions": [],
                "nonce": nonce,
                "previous_hash": "Gawron"
            }

        else:
            lastBlock = self.pg_get_last_block()
            previous_hash = lastBlock["hash"]

            block = {
                "index": len(self.pg_blocks),
                "timestamp": time(),
                "transactions": self.pg_current_transactions.copy(),
                "nonce": 0,
                "previous_hash": previous_hash
            }

            # Proof of Work
            while True:
                hash_value = self.pg_hash(block)

                if hash_value.endswith("0000"):
                    break

                block["nonce"] += 1

        block["hash"] = self.pg_hash(block)

        self.pg_blocks.append(block)
        self.pg_current_transactions = []

        return block

    def pg_get_last_block(self):
        if not self.pg_blocks:
            return None

        return self.pg_blocks[-1]

    def pg_hash(self, lastBlock):
        lastBlock_string = json.dumps(lastBlock, sort_keys=True)
        lastBlock_encoded = lastBlock_string.encode()
        return hashlib.sha256(lastBlock_encoded).hexdigest()