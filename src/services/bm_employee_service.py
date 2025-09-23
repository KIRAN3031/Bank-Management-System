# service/bm_employee_service.py
from typing import Optional, Dict
from src.dao.bm_employee_dao import EmployeeDAO, EmployeeDAOError

class EmployeeServiceError(Exception):
    pass

class EmployeeService:
    def __init__(self):
        self.dao = EmployeeDAO()

    def add_employee(self, name: str, role: str, email: str, phone: Optional[str], password: str) -> Dict:
        try:
            return self.dao.add_employee(name, role, email, phone, password)
        except EmployeeDAOError as e:
            raise EmployeeServiceError(str(e))