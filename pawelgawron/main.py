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

    def pg_hash(self, block):
        data = {
            key: value for key, value in block.items() if key != "hash"
        }

        block_string = json.dumps(data, sort_keys=True)
        block_encoded = block_string.encode()

        return hashlib.sha256(block_encoded).hexdigest()

    def pg_is_chain_valid(self):
        for i in range(len(self.pg_blocks)):
            block = self.pg_blocks[i]

            # 1. Does the hash of the block still match with its data?
            if self.pg_hash(block) != block['hash']:
                print(f"Block {i}: invalid hash!")
                return False

        return True

    def pg_display_chain(self):
        for block in self.pg_blocks:
            print(f"\n--- Block {block['index']} ---")
            print(f"Time: {block['timestamp']}")
            print(f"Transactions: {block['transactions']}")
            print(f"Nonce: {block['nonce']}")
            print(f"Previous hash: {block['previous_hash']}")
            print(f"Hash: {block['hash']}")
            print(
                f"Hash ends with '0000': "
                f"{block['hash'].endswith('0000')}"
            )

if __name__ == "__main__":
    pg_blockchain = Blockchain()

    # The creation of genesis block
    pg_blockchain.pg_add_block()

    pg_blockchain.pg_add_transaction(
        sender="Jan",
        receiver="Ala",
        amount=500
    )

    pg_blockchain.pg_add_block()

    pg_blockchain.pg_display_chain()

    print(f"\nValid chain: {pg_blockchain.pg_is_chain_valid()}")