# dao/bm_employee_dao.py
from typing import Optional, Dict
from src.config import get_supabase
import hashlib

class EmployeeDAOError(Exception):
    pass

class EmployeeDAO:
    def __init__(self):
        self._sb = get_supabase()

    def add_employee(self, name: str, role: str, email: str, phone: Optional[str], password: str) -> Dict:
        if not (name and role and email and password):
            raise EmployeeDAOError("Missing required fields")
        existing = self.get_employee_by_email(email)
        if existing:
            raise EmployeeDAOError("Email already exists")

        # Simple hash, consider stronger hashing in real apps
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        payload = {"name": name, "role": role, "email": email, "phone": phone, "password_hash": password_hash}
        self._sb.table("bm_employees").insert(payload).execute()
        resp = self._sb.table("bm_employees").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_employee_by_email(self, email: str) -> Optional[Dict]:
        resp = self._sb.table("bm_employees").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None

