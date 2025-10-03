from typing import List, Dict
from src.dao.bm_employee_dao import EmployeeDAO, EmployeeDAOError

class EmployeeServiceError(Exception):
    pass

class EmployeeService:
    def __init__(self):
        self.dao = EmployeeDAO()

    def list_employees(self, limit=100) -> List[Dict]:
        try:
            return self.dao.list_employees(limit)
        except EmployeeDAOError as e:
            raise EmployeeServiceError(str(e))

    def create_employee(self, name: str, email: str, phone: str = None, department: str = None) -> Dict:
        try:
            return self.dao.create_employee(name, email, phone, department)
        except EmployeeDAOError as e:
            raise EmployeeServiceError(str(e))