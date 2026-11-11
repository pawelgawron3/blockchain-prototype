from flask import Flask, jsonify, request
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
                "previous_hash": "Gawron",
                "merkle_root": self.pg_merkle_root(
                    self.pg_current_transactions
                ),
            }

        else:
            lastBlock = self.pg_get_last_block()
            previous_hash = lastBlock["hash"]

            block = {
                "index": len(self.pg_blocks),
                "timestamp": time(),
                "transactions": self.pg_current_transactions.copy(),
                "nonce": 0,
                "previous_hash": previous_hash,
                "merkle_root": self.pg_merkle_root(
                    self.pg_current_transactions
                ),
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

            # 2. Check Merkle Root
            calculated_merkle_root = self.pg_merkle_root(
                block["transactions"]
            )
            if calculated_merkle_root != block["merkle_root"]:
                print(f"Block {i}: invalid Merkle Root!")
                return False

        return True

    def pg_merkle_root(self, transactions):
        if not transactions:
            return hashlib.sha256(b"").hexdigest()

        # Hash each transaction
        hashes = []

        for transaction in transactions:
            transaction_string = json.dumps(
                transaction,
                sort_keys=True
            )
            transaction_hash = hashlib.sha256(
                transaction_string.encode()
            ).hexdigest()

            hashes.append(transaction_hash)

        # Build Merkle Tree
        while len(hashes) > 1:
            if len(hashes) % 2 != 0:
                hashes.append(hashes[-1])

            new_level = []

            for i in range(0, len(hashes), 2):
                combined = (
                    bytes.fromhex(hashes[i]) +
                    bytes.fromhex(hashes[i + 1])
                )

                new_hash = hashlib.sha256(combined).hexdigest()
                new_level.append(new_hash)

            hashes = new_level

        return hashes[0]


    def pg_display_chain(self):
        for block in self.pg_blocks:
            print(f"\n--- Block {block['index']} ---")
            print(f"Time: {block['timestamp']}")
            print(f"Transactions: {block['transactions']}")
            print(f"Nonce: {block['nonce']}")
            print(f"Previous hash: {block['previous_hash']}")
            print(f"Hash: {block['hash']}")
            print(f"Merkle Root: {block['merkle_root']}")
            print(
                f"Hash ends with '0000': "
                f"{block['hash'].endswith('0000')}"
            )

app = Flask(__name__)

pg_blockchain = Blockchain()
    
# The creation of genesis block
pg_blockchain.pg_add_block()

@app.route("/chain", methods=["GET"])
def pg_get_chain():
    return jsonify({
        "chain": pg_blockchain.pg_blocks,
        "length": len(pg_blockchain.pg_blocks)
    })

@app.route("/mine", methods=["POST"])
def pg_mine():
    if not pg_blockchain.pg_current_transactions:
        return jsonify({
            "error": "No transactions available to mine!"
        }), 400

    data = request.get_json() or {}
    reward = data.get("reward", 10)

    # Add mining reward
    pg_blockchain.pg_add_transaction(
        "MINING", "Miner", reward
    )

    pg_block = pg_blockchain.pg_add_block()

    return jsonify({
        "message": "New block mined successfully!",
        "block": pg_block,
        "index": pg_block["index"],
        "length": len(pg_blockchain.pg_blocks)
    }), 200


@app.route("/transactions/new", methods=["POST"])
def pg_new_transaction():
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON data"}), 400

    required_fields = ["sender", "receiver", "amount"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing transaction fields"}), 400

    sender = data["sender"]
    receiver = data["receiver"]
    amount = data["amount"]

    if not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"error": "Amount must be a positive number"}), 400

    # Add transaction to mempool
    pg_blockchain.pg_add_transaction(sender, receiver, amount)

    return jsonify({
        "message": "Transaction added successfully!",
        "transaction": pg_blockchain.pg_current_transactions[-1],
        "pending_transactions": len(pg_blockchain.pg_current_transactions)
    }), 201


if __name__ == "__main__":
    app.run(debug=True)