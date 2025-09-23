# service/bm_loan_repayment_service.py
from typing import List, Dict, Optional
from src.dao.bm_loan_repayment_dao import LoanRepaymentDAO, LoanRepaymentDAOError

class LoanRepaymentServiceError(Exception):
    pass

class LoanRepaymentService:
    def __init__(self):
        self.dao = LoanRepaymentDAO()

    def make_repayment(self, loan_id: int, amount: float, payment_date: Optional[str] = None) -> Dict:
        try:
            return self.dao.create_repayment(loan_id, amount, payment_date)
        except LoanRepaymentDAOError as e:
            raise LoanRepaymentServiceError(str(e))

    def list_repayments_for_loan(self, loan_id: int) -> List[Dict]:
        return self.dao.get_repayments_by_loan(loan_id)

    def get_repayment(self, repayment_id: int) -> Optional[Dict]:
        return self.dao.get_repayment_by_id(repayment_id)

    def update_repayment_status(self, repayment_id: int, status: str) -> Optional[Dict]:
        try:
            return self.dao.update_repayment_status(repayment_id, status)
        except LoanRepaymentDAOError as e:
            raise LoanRepaymentServiceError(str(e))