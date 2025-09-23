# dao/bm_loan_repayment_dao.py
from typing import List, Dict, Optional
from src.config import get_supabase

class LoanRepaymentDAOError(Exception):
    pass

class LoanRepaymentDAO:
    def __init__(self):
        self._sb = get_supabase()

    def create_repayment(self, loan_id: int, amount: float, payment_date: Optional[str] = None, status: str = "PAID") -> Dict:
        if amount <= 0:
            raise LoanRepaymentDAOError("Repayment amount must be positive")

        payload = {
            "loan_id": loan_id,
            "amount": amount,
            "payment_date": payment_date or "now()",
            "status": status
        }
        self._sb.table("bm_loan_repayments").insert(payload).execute()
        resp = self._sb.table("bm_loan_repayments").select("*").eq("loan_id", loan_id).order("repayment_id", desc=True).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_repayments_by_loan(self, loan_id: int) -> List[Dict]:
        resp = self._sb.table("bm_loan_repayments").select("*").eq("loan_id", loan_id).order("payment_date", desc=True).execute()
        return resp.data or []

    def get_repayment_by_id(self, repayment_id: int) -> Optional[Dict]:
        resp = self._sb.table("bm_loan_repayments").select("*").eq("repayment_id", repayment_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def update_repayment_status(self, repayment_id: int, status: str) -> Optional[Dict]:
        self._sb.table("bm_loan_repayments").update({"status": status}).eq("repayment_id", repayment_id).execute()
        resp = self._sb.table("bm_loan_repayments").select("*").eq("repayment_id", repayment_id).limit(1).execute()
        return resp.data[0] if resp.data else None


