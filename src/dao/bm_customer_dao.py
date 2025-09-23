# dao/bm_customer_dao.py
from typing import Optional, List, Dict
from src.config import get_supabase

class CustomerDAOError(Exception):
    pass

class CustomerDAO:
    def __init__(self):
        self._sb = get_supabase()

    def create_customer(self, name: str, email: str, phone: Optional[str], city: Optional[str], address: Optional[str]) -> Dict:
        if not name or not email:
            raise CustomerDAOError("Name and email required")
        existing = self.get_customer_by_email(email)
        if existing:
            raise CustomerDAOError(f"Email already exists: {email}")
        payload = {"name": name, "email": email, "phone": phone, "city": city, "address": address}
        self._sb.table("bm_customers").insert(payload).execute()
        resp = self._sb.table("bm_customers").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_customer_by_id(self, cust_id: int) -> Optional[Dict]:
        resp = self._sb.table("bm_customers").select("*").eq("customer_id", cust_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_customer_by_email(self, email: str) -> Optional[Dict]:
        resp = self._sb.table("bm_customers").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None

    def update_customer(self, cust_id: int, fields: Dict) -> Optional[Dict]:
        if not fields:
            raise CustomerDAOError("No fields to update")
        self._sb.table("bm_customers").update(fields).eq("customer_id", cust_id).execute()
        resp = self._sb.table("bm_customers").select("*").eq("customer_id", cust_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def delete_customer(self, cust_id: int) -> Optional[Dict]:
        accounts_resp = self._sb.table("bm_accounts").select("*").eq("customer_id", cust_id).limit(1).execute()
        loans_resp = self._sb.table("bm_loans").select("*").eq("customer_id", cust_id).limit(1).execute()
        if accounts_resp.data or loans_resp.data:
            raise CustomerDAOError("Cannot delete customer with existing accounts or loans.")
        resp_before = self._sb.table("bm_customers").select("*").eq("customer_id", cust_id).limit(1).execute()
        row = resp_before.data[0] if resp_before.data else None
        self._sb.table("bm_customers").delete().eq("customer_id", cust_id).execute()
        return row

    def list_customers(self, limit: int = 100) -> List[Dict]:
        resp = self._sb.table("bm_customers").select("*").order("customer_id", desc=False).limit(limit).execute()
        return resp.data or []

    def search_customers(self, email: Optional[str] = None, city: Optional[str] = None) -> List[Dict]:
        q = self._sb.table("bm_customers").select("*")
        if email:
            q = q.eq("email", email)
        if city:
            q = q.eq("city", city)
        resp = q.execute()
        return resp.data or []