import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wallet import Wallet
from transaction import Transaction, TransactionPool
from blockchain import Blockchain, Block

class TestWallet(unittest.TestCase):
    def setUp(self):
        self.wallet = Wallet("my_private_key_123", "password123")

    def test_generate_address(self):
        address = self.wallet.generate_address()
        self.assertIsNotNone(address)
        self.assertEqual(len(address), 34)

    def test_authenticate_success(self):
        result = self.wallet.authenticate("password123")
        self.assertTrue(result)

    def test_authenticate_failure(self):
        result = self.wallet.authenticate("wrong_password")
        self.assertFalse(result)

    def test_add_funds(self):
        result = self.wallet.add_funds(100.0)
        self.assertTrue(result)
        self.assertEqual(self.wallet.get_balance(), 100.0)

    def test_transfer_success(self):
        self.wallet.add_funds(100.0)
        result = self.wallet.transfer("recipient_address", 50.0)
        self.assertTrue(result["success"])
        self.assertEqual(self.wallet.get_balance(), 50.0)

    def test_transfer_insufficient_balance(self):
        self.wallet.add_funds(50.0)
        result = self.wallet.transfer("recipient_address", 100.0)
        self.assertFalse(result["success"])
        self.assertIn("Insufficient balance", result["error"])

class TestTransaction(unittest.TestCase):
    def test_transaction_creation(self):
        tx = Transaction("sender", "recipient", 100.0)
        self.assertIsNotNone(tx.tx_hash)
        self.assertEqual(tx.amount, 100.0)

    def test_transaction_confirm(self):
        tx = Transaction("sender", "recipient", 100.0)
        tx.confirm()
        self.assertEqual(tx.status.value, "confirmed")

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.blockchain = Blockchain()

    def test_genesis_block(self):
        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(self.blockchain.chain[0].index, 0)

    def test_add_transaction(self):
        tx = Transaction("sender", "recipient", 100.0)
        result = self.blockchain.add_transaction(tx)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
