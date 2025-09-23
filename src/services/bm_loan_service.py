# service/bm_loan_service.py
from typing import Optional, Dict
from src.dao.bm_loan_dao import LoanDAO, LoanDAOError

class LoanServiceError(Exception):
    pass

class LoanService:
    def __init__(self):
        self.dao = LoanDAO()

    def apply_for_loan(self, customer_id: int, loan_type: str, amount: float, interest_rate: float) -> Dict:
        try:
            return self.dao.apply_loan(customer_id, loan_type, amount, interest_rate)
        except LoanDAOError as e:
            raise LoanServiceError(str(e))

    def repay_loan(self, loan_id: int, amount: float) -> Dict:
        try:
            return self.dao.repay_loan(loan_id, amount)
        except LoanDAOError as e:
            raise LoanServiceError(str(e))

    def get_loan_status(self, loan_id: int) -> Optional[Dict]:
        return self.dao.get_loan_by_id(loan_id)