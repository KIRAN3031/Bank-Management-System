# dao/bm_account_dao.py
from typing import List, Dict, Optional
from src.config import get_supabase

class AccountDAOError(Exception):
    pass

class AccountDAO:
    def __init__(self):
        self._sb = get_supabase()

    def open_account(self, customer_id: int, account_type: str) -> Dict:
        if not customer_id or not account_type:
            raise AccountDAOError("customer_id and account_type are required")
        payload = {"customer_id": customer_id, "account_type": account_type, "balance": 0, "status": "ACTIVE"}
        self._sb.table("bm_accounts").insert(payload).execute()
        resp = self._sb.table("bm_accounts").select("*").eq("customer_id", customer_id).order("account_id", desc=True).limit(1).execute()
        return resp.data[0] if resp.data else None

    def close_account(self, account_id: int) -> Optional[Dict]:
        account = self._sb.table("bm_accounts").select("*").eq("account_id", account_id).limit(1).execute()
        if not account.data or account.data[0].get("balance", 0) != 0:
            raise AccountDAOError("Account must have zero balance to close")
        self._sb.table("bm_accounts").update({"status": "CLOSED"}).eq("account_id", account_id).execute()
        resp = self._sb.table("bm_accounts").select("*").eq("account_id", account_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def list_accounts_by_customer(self, customer_id: int) -> List[Dict]:
        resp = self._sb.table("bm_accounts").select("*").eq("customer_id", customer_id).execute()
        return resp.data or []
