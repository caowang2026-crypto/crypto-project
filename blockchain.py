import hashlib
import time
from typing import List, Optional
from transaction import Transaction, TransactionPool
from typing import List

class Block:
    def __init__(self, index: int, timestamp: float, transactions: List[Transaction], previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        data = f"{self.index}{self.timestamp}{[tx.to_dict() for tx in self.transactions]}{self.previous_hash}"
        return hashlib.sha256(data.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions: List[Transaction] = []
        self.mining_reward = 10.0

    def create_genesis_block(self) -> Block:
        return Block(0, time.time(), [], "0" * 64)

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def mine_pending_transactions(self, miner_address: str) -> bool:
        if not self.pending_transactions:
            return False

        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=self.pending_transactions,
            previous_hash=self.get_latest_block().hash
        )

        if self.proof_of_work(new_block):
            self.chain.append(new_block)
            reward_tx = Transaction("system", miner_address, self.mining_reward)
            self.pending_transactions = []
            return True

        return False

    def proof_of_work(self, block: Block) -> bool:
        target = "0" * self.difficulty
        while block.hash[:self.difficulty] != target:
            block.timestamp = time.time()
            block.hash = block.calculate_hash()
        return True

    def add_transaction(self, tx: Transaction) -> bool:
        if not self.is_valid_transaction(tx):
            return False
        self.pending_transactions.append(tx)
        return True

    def is_valid_transaction(self, tx: Transaction) -> bool:
        if tx.amount <= 0:
            return False
        if tx.from_address == "system":
            return True
        return tx.calculate_hash() == tx.tx_hash

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def get_balance(self, address: str) -> float:
        balance = 0.0

        for block in self.chain:
            for tx in block.transactions:
                if tx.from_address == address:
                    balance -= tx.amount
                if tx.to_address == address:
                    balance += tx.amount

        for tx in self.pending_transactions:
            if tx.from_address == address:
                balance -= tx.amount
            if tx.to_address == address:
                balance += tx.amount

        return balance
