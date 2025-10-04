from typing import List, Dict
from src.dao.bm_transaction_dao import TransactionDAO, TransactionDAOError

class TransactionServiceError(Exception):
    pass

class TransactionService:
    def __init__(self):
        self.dao = TransactionDAO()

    def deposit(self, account_id: int, amount: float) -> Dict:
        try:
            return self.dao.deposit(account_id, amount)
        except TransactionDAOError as e:
            raise TransactionServiceError(str(e))

    def withdraw(self, account_id: int, amount: float) -> Dict:
        try:
            return self.dao.withdraw(account_id, amount)
        except TransactionDAOError as e:
            raise TransactionServiceError(str(e))

    def transfer(self, from_account_id: int, to_account_id: int, amount: float) -> Dict:
        try:
            return self.dao.transfer(from_account_id, to_account_id, amount)
        except TransactionDAOError as e:
            raise TransactionServiceError(str(e))

    def get_transaction_history(self, account_id: int) -> List[Dict]:
        return self.dao.get_transactions_by_account(account_id)

    def get_all_transactions(self) -> List[Dict]:
        try:
            return self.dao.get_all_transactions()
        except TransactionDAOError as e:
            raise TransactionServiceError(str(e))