# dao/bm_loan_dao.py
from typing import Optional, Dict, List
from src.config import get_supabase

class LoanDAOError(Exception):
    pass

class LoanDAO:
    def __init__(self):
        self._sb = get_supabase()

    def apply_loan(self, customer_id: int, loan_type: str, amount: float, interest_rate: float) -> Dict:
        if not (customer_id and loan_type and amount > 0):
            raise LoanDAOError("Invalid loan application data")
        payload = {
            "customer_id": customer_id,
            "loan_type": loan_type,
            "amount": amount,
            "interest_rate": interest_rate,
            "status": "PENDING"
        }
        # Log payload for debugging
        print("Applying for loan with payload:", payload)
        try:
            self._sb.table("bm_loans").insert(payload).execute()
        except Exception as e:
            # Raise error with detailed message
            raise LoanDAOError(f"Failed to apply for loan: {e}")
        resp = self._sb.table("bm_loans").select("*").eq("customer_id", customer_id).order("loan_id", desc=True).limit(1).execute()
        return resp.data[0] if resp.data else None

    def repay_loan(self, loan_id: int, amount: float) -> Dict:
        # Implementation detail can be enhanced with balance checks, repayment schedule
        if amount <= 0:
            raise LoanDAOError("Repayment amount must be positive")
        # For simplicity, record a repayment entry in bm_loan_repayments and update loan status if fully repaid
        repayment_payload = {"loan_id": loan_id, "amount": amount, "payment_date": "now()", "status": "PAID"}
        self._sb.table("bm_loan_repayments").insert(repayment_payload).execute()
        # Assuming loan status update happens elsewhere, return repayment record here
        resp = self._sb.table("bm_loan_repayments").select("*").eq("loan_id", loan_id).order("repayment_id", desc=True).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_loan_by_id(self, loan_id: int) -> Optional[Dict]:
        resp = self._sb.table("bm_loans").select("*").eq("loan_id", loan_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_loans_by_customer(self, customer_id: int) -> List[Dict]:
        try:
            resp = self._sb.table("bm_loans").select("*").eq("customer_id", customer_id).execute()
            return resp.data or []
        except Exception as e:
            raise LoanDAOError(f"Failed to fetch loans for customer {customer_id}: {e}")

    def get_all_loans(self) -> List[Dict]:
        try:
            resp = self._sb.table("bm_loans").select("*").execute()
            return resp.data or []
        except Exception as e:
            raise LoanDAOError(f"Failed to fetch all loans: {e}")