import hashlib
import time
from typing import List, Dict, Optional
from enum import Enum

class TransactionStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"

class Transaction:
    def __init__(self, from_address: str, to_address: str, amount: float, fee: float = 0.0001):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.fee = fee
        self.status = TransactionStatus.PENDING
        self.timestamp = time.time()
        self.tx_hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        data = f"{self.from_address}{self.to_address}{self.amount}{self.timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()

    def confirm(self):
        self.status = TransactionStatus.CONFIRMED

    def to_dict(self) -> Dict:
        return {
            "tx_hash": self.tx_hash,
            "from": self.from_address,
            "to": self.to_address,
            "amount": self.amount,
            "fee": self.fee,
            "status": self.status.value,
            "timestamp": self.timestamp
        }

class TransactionPool:
    def __init__(self):
        self.pending_transactions: List[Transaction] = []

    def add_transaction(self, tx: Transaction) -> bool:
        if tx.amount <= 0:
            return False

        for existing_tx in self.pending_transactions:
            if existing_tx.tx_hash == tx.tx_hash:
                return False

        self.pending_transactions.append(tx)
        return True

    def get_pending_transactions(self) -> List[Transaction]:
        return self.pending_transactions.copy()

    def confirm_transaction(self, tx_hash: str) -> bool:
        for tx in self.pending_transactions:
            if tx.tx_hash == tx_hash:
                tx.confirm()
                self.pending_transactions.remove(tx)
                return True
        return False

    def get_transaction_by_hash(self, tx_hash: str) -> Optional[Transaction]:
        for tx in self.pending_transactions:
            if tx.tx_hash == tx_hash:
                return tx
        return None
