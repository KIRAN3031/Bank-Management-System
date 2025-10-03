import os
import streamlit as st
from src.services.bm_customer_service import CustomerService, CustomerServiceError
from src.services.bm_account_service import AccountService, AccountServiceError
from src.services.bm_transaction_service import TransactionService, TransactionServiceError
from src.services.bm_loan_service import LoanService, LoanServiceError
from src.services.bm_loan_repayment_service import LoanRepaymentService, LoanRepaymentServiceError

# Initialize services
customer_service = CustomerService()
account_service = AccountService()
transaction_service = TransactionService()
loan_service = LoanService()
loan_repayment_service = LoanRepaymentService()

st.title("Bank Management System")

# Sidebar for navigation
menu = st.sidebar.selectbox("Menu", [
    "View Customers",
    "Add Customer",
    "View Accounts",
    "Open Account",
    "Deposit",
    "Withdraw",
    "Transfer",
    "Apply Loan",
    "Repay Loan",
    "View Loans"
])

# --- View Customers ---
if menu == "View Customers":
    st.header("Customers")
    if st.button("Refresh Customers"):
        pass
    try:
        customers = customer_service.list_customers()
        for c in customers:
            st.write(f"**ID {c['customer_id']}**: {c['name']} — {c['email']} — {c['phone']} — {c['city']}")
    except CustomerServiceError as e:
        st.error(f"Failed to load customers: {e}")

# --- Add Customer ---
elif menu == "Add Customer":
    st.header("Add New Customer")
    with st.form("add_customer"):
        name = st.text_input("Name", key="add_name")
        email = st.text_input("Email", key="add_email")
        phone = st.text_input("Phone", key="add_phone")
        city = st.text_input("City", key="add_city")
        address = st.text_area("Address", key="add_address")
        if st.form_submit_button("Add Customer"):
            try:
                customer_service.create_customer(name, email, phone, city, address)
                st.success("Customer added successfully!")
            except CustomerServiceError as e:
                st.error(f"Failed to add customer: {e}")

# --- View Accounts ---
elif menu == "View Accounts":
    st.header("Accounts")
    customer_id = st.number_input("Enter Customer ID", min_value=1, step=1)
    if st.button("Load Accounts"):
        try:
            accounts = account_service.list_accounts(customer_id)
            if accounts:
                for a in accounts:
                    st.write(f"**Account {a['account_id']}**: {a['account_type']} — Balance: ₹{a['balance']} — Status: {a['status']}")
            else:
                st.info("No accounts found for this customer.")
        except AccountServiceError as e:
            st.error(f"Failed to load accounts: {e}")

# --- Open Account ---
elif menu == "Open Account":
    st.header("Open New Account")
    with st.form("open_account"):
        customer_id = st.number_input("Customer ID", min_value=1, step=1)
        account_type = st.selectbox("Account Type", ["Savings", "Checking"])
        if st.form_submit_button("Open Account"):
            try:
                account_service.open_account(customer_id, account_type)
                st.success("Account opened successfully!")
            except AccountServiceError as e:
                st.error(f"Failed to open account: {e}")

# --- Deposit ---
elif menu == "Deposit":
    st.header("Deposit Money")
    with st.form("deposit"):
        account_id = st.number_input("Account ID", min_value=1, step=1)
        amount = st.number_input("Amount", min_value=0.01, step=0.01, format="%.2f")
        if st.form_submit_button("Deposit"):
            try:
                transaction_service.deposit(account_id, amount)
                st.success(f"₹{amount} deposited successfully!")
            except TransactionServiceError as e:
                st.error(f"Deposit failed: {e}")

# --- Withdraw ---
elif menu == "Withdraw":
    st.header("Withdraw Money")
    with st.form("withdraw"):
        account_id = st.number_input("Account ID", min_value=1, step=1)
        amount = st.number_input("Amount", min_value=0.01, step=0.01, format="%.2f")
        if st.form_submit_button("Withdraw"):
            try:
                transaction_service.withdraw(account_id, amount)
                st.success(f"₹{amount} withdrawn successfully!")
            except TransactionServiceError as e:
                st.error(f"Withdrawal failed: {e}")

# --- Transfer ---
elif menu == "Transfer":
    st.header("Transfer Money")
    with st.form("transfer"):
        from_account_id = st.number_input("From Account ID", min_value=1, step=1)
        to_account_id = st.number_input("To Account ID", min_value=1, step=1)
        amount = st.number_input("Amount", min_value=0.01, step=0.01, format="%.2f")
        if st.form_submit_button("Transfer"):
            try:
                transaction_service.transfer(from_account_id, to_account_id, amount)
                st.success(f"₹{amount} transferred successfully!")
            except TransactionServiceError as e:
                st.error(f"Transfer failed: {e}")

# --- Apply Loan ---
elif menu == "Apply Loan":
    st.header("Apply for Loan")
    with st.form("apply_loan"):
        customer_id = st.number_input("Customer ID", min_value=1, step=1)
        loan_type = st.selectbox("Loan Type", ["Personal", "Home", "Car", "Education"])
        amount = st.number_input("Loan Amount", min_value=1000.0, step=1000.0, format="%.2f")
        interest_rate = st.number_input("Interest Rate (%)", min_value=1.0, max_value=20.0, step=0.1, format="%.2f")
        if st.form_submit_button("Apply"):
            try:
                loan_service.apply_for_loan(customer_id, loan_type, amount, interest_rate)
                st.success("Loan application submitted!")
            except LoanServiceError as e:
                st.error(f"Loan application failed: {e}")

# --- Repay Loan ---
elif menu == "Repay Loan":
    st.header("Repay Loan")
    with st.form("repay_loan"):
        loan_id = st.number_input("Loan ID", min_value=1, step=1)
        amount = st.number_input("Repayment Amount", min_value=0.01, step=0.01, format="%.2f")
        if st.form_submit_button("Repay"):
            try:
                loan_repayment_service.make_repayment(loan_id, amount)
                st.success(f"Loan repayment of ₹{amount} successful!")
            except LoanRepaymentServiceError as e:
                st.error(f"Repayment failed: {e}")

# --- View Loans ---
elif menu == "View Loans":
    st.header("Loans")
    customer_id = st.number_input("Enter Customer ID", min_value=1, step=1)
    if st.button("Load Loans"):
        try:
            # Assuming you have a method to list loans by customer
            # If not, you can add it to LoanService
            loans = loan_service.get_loan_status_by_customer(customer_id)  # You may need to implement this
            if loans:
                for l in loans:
                    st.write(f"**Loan {l['loan_id']}**: {l['loan_type']} — Amount: ₹{l['amount']} — Rate: {l['interest_rate']}% — Status: {l['status']}")
            else:
                st.info("No loans found for this customer.")
        except Exception as e:
            st.error(f"Failed to load loans: {e}")