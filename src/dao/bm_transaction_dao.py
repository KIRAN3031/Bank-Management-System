# dao/bm_transaction_dao.py
from typing import List, Dict, Optional
from src.config import get_supabase

class TransactionDAOError(Exception):
    pass

class TransactionDAO:
    def __init__(self):
        self._sb = get_supabase()

    def deposit(self, account_id: int, amount: float) -> Dict:
        if amount <= 0:
            raise TransactionDAOError("Deposit amount must be positive")
        # Add deposit transaction
        payload = {
            "account_id": account_id,
            "transaction_type": "DEPOSIT",
            "amount": amount,
            "transaction_date": "now()"
        }
        self._sb.table("bm_transactions").insert(payload).execute()
        # Update account balance
        account_resp = self._sb.table("bm_accounts").select("*").eq("account_id", account_id).limit(1).execute()
        if not account_resp.data:
            raise TransactionDAOError("Account not found")
        account = account_resp.data[0]
        new_balance = (account.get("balance") or 0) + amount
        self._sb.table("bm_accounts").update({"balance": new_balance}).eq("account_id", account_id).execute()
        return {"account_id": account_id, "new_balance": new_balance, "transaction": payload}

    def withdraw(self, account_id: int, amount: float) -> Dict:
        if amount <= 0:
            raise TransactionDAOError("Withdraw amount must be positive")
        account_resp = self._sb.table("bm_accounts").select("*").eq("account_id", account_id).limit(1).execute()
        if not account_resp.data:
            raise TransactionDAOError("Account not found")
        account = account_resp.data[0]
        current_balance = account.get("balance") or 0
        if current_balance < amount:
            raise TransactionDAOError("Insufficient balance")
        # Add withdrawal transaction
        payload = {
            "account_id": account_id,
            "transaction_type": "WITHDRAW",
            "amount": amount,
            "transaction_date": "now()"
        }
        self._sb.table("bm_transactions").insert(payload).execute()
        # Update account balance
        new_balance = current_balance - amount
        self._sb.table("bm_accounts").update({"balance": new_balance}).eq("account_id", account_id).execute()
        return {"account_id": account_id, "new_balance": new_balance, "transaction": payload}

    def transfer(self, from_account_id: int, to_account_id: int, amount: float) -> Dict:
        if amount <= 0:
            raise TransactionDAOError("Transfer amount must be positive")
        # Withdraw from source account
        self.withdraw(from_account_id, amount)
        # Deposit to destination account
        self.deposit(to_account_id, amount)
        # Return summary
        return {
            "from_account_id": from_account_id,
            "to_account_id": to_account_id,
            "amount": amount
        }

    def get_transactions_by_account(self, account_id: int) -> List[Dict]:
        resp = self._sb.table("bm_transactions").select("*").eq("account_id", account_id).order("transaction_date", desc=True).execute()
        return resp.data or []


