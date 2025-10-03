from typing import List, Dict
from src.config import get_supabase

class EmployeeDAOError(Exception):
    pass

class EmployeeDAO:
    def __init__(self):
        self._sb = get_supabase()

    def list_employees(self, limit: int = 100) -> List[Dict]:
        try:
            resp = self._sb.table("bm_employees").select("*").order("employee_id", desc=False).limit(limit).execute()
            return resp.data or []
        except Exception as e:
            raise EmployeeDAOError(f"Failed to list employees: {e}")

    def create_employee(self, name: str, email: str, phone: str = None, department: str = None) -> Dict:
        try:
            emp = {
                "name": name,
                "email": email,
                "phone": phone,
                "department": department
            }
            resp = self._sb.table("bm_employees").insert(emp).execute()
            if resp.status_code != 201:
                raise EmployeeDAOError(f"Insert failed: {resp.data}")
            return resp.data[0]
        except Exception as e:
            raise EmployeeDAOError(f"Failed to create employee: {e}")