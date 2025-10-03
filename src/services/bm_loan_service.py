# service/bm_loan_service.py
from typing import List, Dict
from src.dao.bm_loan_dao import LoanDAO, LoanDAOError

class LoanServiceError(Exception):
    pass

class LoanService:
    # initialize the service with DAO
    def __init__(self):
        self.dao = LoanDAO()

    # apply for a loan
    def apply_for_loan(self, customer_id: int, loan_type: str, amount: float, interest_rate: float) -> Dict:
        try:
            return self.dao.apply_loan(customer_id, loan_type, amount, interest_rate)
        except LoanDAOError as e:
            raise LoanServiceError(str(e))
        
    # repay loan
    def repay_loan(self, loan_id: int, amount: float) -> Dict:
        try:
            return self.dao.repay_loan(loan_id, amount)
        except LoanDAOError as e:
            raise LoanServiceError(str(e))
        
    # get loan by id
    def get_loan_status(self, loan_id: int) -> Dict:
        return self.dao.get_loan_by_id(loan_id)

    # get loans by customer
    def get_loan_status_by_customer(self, customer_id: int) -> List[Dict]:
        return self.dao.get_loans_by_customer(customer_id)
    
    # get all loans
    def get_all_loans(self) -> List[Dict]:
        try:
            return self.dao.get_all_loans()
        except LoanDAOError as e:
            raise LoanServiceError(str(e))