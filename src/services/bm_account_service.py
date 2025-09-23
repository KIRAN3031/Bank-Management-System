# service/bm_account_service.py
from typing import List, Dict, Optional
from src.dao.bm_account_dao import AccountDAO, AccountDAOError

class AccountServiceError(Exception):
    pass

class AccountService:
    def __init__(self):
        self.dao = AccountDAO()

    def open_account(self, customer_id: int, account_type: str) -> Dict:
        try:
            return self.dao.open_account(customer_id, account_type)
        except AccountDAOError as e:
            raise AccountServiceError(str(e))

    def close_account(self, account_id: int) -> Optional[Dict]:
        try:
            return self.dao.close_account(account_id)
        except AccountDAOError as e:
            raise AccountServiceError(str(e))

    def list_accounts(self, customer_id: int) -> List[Dict]:
        return self.dao.list_accounts_by_customer(customer_id)