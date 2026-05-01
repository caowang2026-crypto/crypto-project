import hashlib
import hmac
import base64
from typing import Optional, Dict, Any
import json

class Wallet:
    def __init__(self, private_key: str, password: str):
        self.private_key = private_key
        self.password = password
        self.balance = 0.0
        self.address = self.generate_address()

    def generate_address(self) -> str:
        hash_obj = hashlib.sha256(self.private_key.encode())
        return base64.b64encode(hash_obj.digest()).decode()[:34]

    def authenticate(self, password: str) -> bool:
        return self.password == password

    def get_balance(self) -> float:
        return self.balance

    def add_funds(self, amount: float) -> bool:
        if amount <= 0:
            return False
        self.balance += amount
        return True

    def transfer(self, to_address: str, amount: float) -> Dict[str, Any]:
        if amount <= 0:
            return {"success": False, "error": "Invalid amount"}

        if amount > self.balance:
            return {"success": False, "error": "Insufficient balance"}

        self.balance -= amount
        return {
            "success": True,
            "from": self.address,
            "to": to_address,
            "amount": amount,
            "tx_hash": hashlib.sha256(f"{self.address}{to_address}{amount}".encode()).hexdigest()
        }

    def export_private_key(self) -> str:
        return self.private_key
