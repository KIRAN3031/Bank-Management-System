import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from typing import Optional, Dict
from src.services.bm_customer_service import CustomerService, CustomerServiceError
from src.services.bm_account_service import AccountService, AccountServiceError
from src.services.bm_transaction_service import TransactionService, TransactionServiceError
from src.services.bm_loan_service import LoanService, LoanServiceError
from src.services.bm_loan_repayment_service import LoanRepaymentService, LoanRepaymentServiceError
from src.services.bm_employee_service import EmployeeService, EmployeeServiceError


st.title("Bank Management System")

# Initialize all services
customer_service = CustomerService()
account_service = AccountService()
transaction_service = TransactionService()
loan_service = LoanService()
loan_repayment_service = LoanRepaymentService()
employee_service = EmployeeService()


def load_customers():
    try:
        return customer_service.list_customers()
    except CustomerServiceError as e:
        st.error(f"Failed to load customers: {e}")
        return []


def load_accounts(customer_id=None):
    try:
        if customer_id:
            return account_service.list_accounts(customer_id)
        else:
            # Assuming you have a method to list all accounts if no customer_id given
            return account_service.list_all_accounts()
    except AccountServiceError as e:
        st.error(f"Failed to load accounts: {e}")
        return []


def load_loans(customer_id=None):
    try:
        if customer_id:
            return loan_service.get_loan_status_by_customer(customer_id)
        else:
            return loan_service.get_all_loans()
    except LoanServiceError as e:
        st.error(f"Failed to load loans: {e}")
        return []


def load_transactions(account_id=None):
    try:
        if account_id:
            return transaction_service.get_transaction_history(account_id)
        else:
            return transaction_service.get_all_transactions()
    except TransactionServiceError as e:
        st.error(f"Failed to load transactions: {e}")
        return []


def load_repayments(loan_id=None):
    try:
        if loan_id:
            return loan_repayment_service.list_repayments_for_loan(loan_id)
        else:
            return loan_repayment_service.list_all_repayments()
    except LoanRepaymentServiceError as e:
        st.error(f"Failed to load repayments: {e}")
        return []


def load_employees():
    try:
        return employee_service.list_employees()
    except EmployeeServiceError as e:
        st.error(f"Failed to load employees: {e}")
        return []


def dashboard():
    st.header("📊 Dashboard")

    # Gather data without filtering for dashboard overview
    customers = load_customers()
    accounts = load_accounts()
    loans = load_loans()
    transactions = load_transactions()
    repayments = load_repayments()
    employees_list = load_employees()

    df_customers = pd.DataFrame(customers)
    df_accounts = pd.DataFrame(accounts)
    df_loans = pd.DataFrame(loans)
    df_transactions = pd.DataFrame(transactions)
    df_repayments = pd.DataFrame(repayments)
    employees = pd.DataFrame(employees_list)

    # Metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Customers", len(df_customers))
    col2.metric("Active Accounts", len(df_accounts[df_accounts['status'] == "Active"]) if not df_accounts.empty else 0)
    col3.metric("Total Loans", len(df_loans))
    col4.metric("Transactions", len(df_transactions))
    col5.metric("Repayments", len(df_repayments))

    # Pie Chart: Account Type Distribution
    if not df_accounts.empty and 'account_type' in df_accounts.columns:
        account_types = df_accounts['account_type'].value_counts()
        fig = go.Figure(data=[go.Pie(labels=account_types.index, values=account_types.values, hole=0.4)])
        st.subheader("Account Types Distribution")
        st.plotly_chart(fig, use_container_width=True)

    # Bar Chart: Loans by Type
    if not df_loans.empty and 'loan_type' in df_loans.columns:
        loan_types = df_loans['loan_type'].value_counts()
        colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3']  # Add more colors if needed
        fig = go.Figure(data=[go.Bar(
            x=loan_types.index,
            y=loan_types.values,
            marker_color=colors[:len(loan_types)]  # Slice to match number of bars
        )])
        st.subheader("Loans by Type")
        st.plotly_chart(fig, use_container_width=True)

    # Line Chart: Monthly Transactions Trend by Type
    if not df_transactions.empty and 'transaction_date' in df_transactions.columns:
        df_transactions['transaction_date'] = pd.to_datetime(df_transactions['transaction_date'], errors='coerce', utc=True)
        df_transactions['transaction_date'] = df_transactions['transaction_date'].dt.tz_localize(None)  # Remove timezone
        df_transactions['month'] = df_transactions['transaction_date'].dt.to_period('M')
        trend_data = df_transactions.groupby(['month', 'transaction_type']).size().unstack(fill_value=0)
        fig = go.Figure()
        for transaction_type in trend_data.columns:
            fig.add_trace(go.Scatter(x=trend_data.index.astype(str), y=trend_data[transaction_type], mode='lines+markers', name=transaction_type))
        st.subheader("Monthly Transaction Trend")
        st.plotly_chart(fig, use_container_width=True)

    # Pie Chart: Loan Repayment Status
    if not df_repayments.empty and 'status' in df_repayments.columns:
        repayment_status = df_repayments['status'].value_counts()
        fig = go.Figure(data=[go.Pie(labels=repayment_status.index, values=repayment_status.values)])
        st.subheader("Loan Repayment Status")
        st.plotly_chart(fig, use_container_width=True)

    # Bar Chart: Employee roles distribution
    if not employees.empty and 'role' in employees.columns:
        role_counts = employees['role'].value_counts()
        colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3']
        fig = go.Figure(data=[go.Bar(
            x=role_counts.index,
            y=role_counts.values,
            marker_color=colors[:len(role_counts)]
        )])
        st.subheader("Employee Roles Distribution")
        st.plotly_chart(fig, use_container_width=True)

    # Interactive Table Selector
    st.subheader("View Raw Data")
    table_option = st.selectbox("Select Table to View", options=["Customers", "Accounts", "Loans", "Transactions", "Repayments", "Employees"])
    if table_option == "Customers":
        st.dataframe(df_customers)
    elif table_option == "Accounts":
        st.dataframe(df_accounts)
    elif table_option == "Loans":
        st.dataframe(df_loans)
    elif table_option == "Transactions":
        st.dataframe(df_transactions)
    elif table_option == "Repayments":
        st.dataframe(df_repayments)
    elif table_option == "Employees":
        employees = load_employees()
        st.dataframe(pd.DataFrame(employees))


def main():
    menu = st.sidebar.selectbox("Menu", ["Dashboard", "Customers", "Accounts", "Loans", "Transactions", "Loan Repayments", "Employees"])

    if menu == "Dashboard":
        dashboard()

    elif menu == "Customers":
        st.header("Customers")
        customers = load_customers()
        st.dataframe(customers)
        with st.expander("Add Customer"):
            with st.form("add_customer"):
                name = st.text_input("Name")
                email = st.text_input("Email")
                phone = st.text_input("Phone")
                city = st.text_input("City")
                address = st.text_area("Address")
                submit = st.form_submit_button("Add")
                if submit:
                    try:
                        customer_service.create_customer(name, email, phone or None, city or None, address or None)
                        st.success("Customer added successfully!")
                    except CustomerServiceError as e:
                        st.error(f"Failed to add customer: {e}")

    elif menu == "Accounts":
        st.header("Accounts")
        customers = load_customers()
        cust_options = [f"{c['customer_id']} - {c['name']}" for c in customers]
        selected_cust = st.selectbox("Select Customer", cust_options)
        if selected_cust:
            cust_id = int(selected_cust.split(" - ")[0])
            accounts = load_accounts(cust_id)
            st.dataframe(accounts)
            with st.expander("Open Account"):
                with st.form("open_account"):
                    account_type = st.selectbox("Account Type", ["Savings", "Checking", "Current"])
                    submit = st.form_submit_button("Open Account")
                    if submit:
                        try:
                            account_service.open_account(cust_id, account_type)
                            st.success("Account opened successfully!")
                        except AccountServiceError as e:
                            st.error(f"Failed to open account: {e}")

    elif menu == "Loans":
        st.header("Loans")
        customers = load_customers()
        cust_options = [f"{c['customer_id']} - {c['name']}" for c in customers]
        selected_cust = st.selectbox("Select Customer", cust_options)
        if selected_cust:
            cust_id = int(selected_cust.split(" - ")[0])
            loans = load_loans(cust_id)
            st.dataframe(loans)
            with st.expander("Apply Loan"):
                with st.form("apply_loan"):
                    loan_type = st.text_input("Loan Type")
                    amount = st.number_input("Amount", min_value=0.01, format="%.2f")
                    interest_rate = st.number_input("Interest Rate (%)", min_value=0.01, format="%.2f")
                    submit = st.form_submit_button("Apply")
                    if submit:
                        try:
                            loan_service.apply_for_loan(cust_id, loan_type, amount, interest_rate)
                            st.success("Loan application submitted!")
                        except LoanServiceError as e:
                            st.error(f"Failed to apply loan: {e}")

    elif menu == "Transactions":
        st.header("Transactions")
        customers = load_customers()
        cust_options = [f"{c['customer_id']} - {c['name']}" for c in customers]
        selected_cust = st.selectbox("Select Customer", cust_options)
        if selected_cust:
            cust_id = int(selected_cust.split(" - ")[0])
            accounts = load_accounts(cust_id)
            acc_options = [f"{a['account_id']} - {a['account_type']}" for a in accounts]
            selected_acc = st.selectbox("Select Account", acc_options)
            if selected_acc:
                acc_id = int(selected_acc.split(" - ")[0])
                transactions = load_transactions(acc_id)
                st.dataframe(transactions)
                st.subheader("Deposit Money")
                with st.form("deposit_form"):
                    dep_amount = st.number_input("Deposit Amount", min_value=0.01, format="%.2f")
                    dep_submit = st.form_submit_button("Deposit")
                    if dep_submit:
                        try:
                            transaction_service.deposit(acc_id, dep_amount)
                            st.success("Deposit successful!")
                        except TransactionServiceError as e:
                            st.error(f"Deposit failed: {e}")

                st.subheader("Withdraw Money")
                with st.form("withdraw_form"):
                    wd_amount = st.number_input("Withdraw Amount", min_value=0.01, format="%.2f")
                    wd_submit = st.form_submit_button("Withdraw")
                    if wd_submit:
                        try:
                            transaction_service.withdraw(acc_id, wd_amount)
                            st.success("Withdrawal successful!")
                        except TransactionServiceError as e:
                            st.error(f"Withdrawal failed: {e}")

                st.subheader("Transfer Money")
                with st.form("transfer_form"):
                    to_acc = st.number_input("To Account ID", min_value=1)
                    trans_amount = st.number_input("Transfer Amount", min_value=0.01, format="%.2f")
                    trans_submit = st.form_submit_button("Transfer")
                    if trans_submit:
                        try:
                            transaction_service.transfer(acc_id, int(to_acc), trans_amount)
                            st.success("Transfer successful!")
                        except TransactionServiceError as e:
                            st.error(f"Transfer failed: {e}")

    elif menu == "Loan Repayments":
        st.header("Loan Repayments")
        customers = load_customers()
        cust_options = [f"{c['customer_id']} - {c['name']}" for c in customers]
        selected_cust = st.selectbox("Select Customer", cust_options)
        if selected_cust:
            cust_id = int(selected_cust.split(" - ")[0])
            loans = load_loans(cust_id)
            loan_options = [f"{l['loan_id']} - {l['loan_type']}" for l in loans]
            selected_loan = st.selectbox("Select Loan", loan_options)
            if selected_loan:
                loan_id = int(selected_loan.split(" - ")[0])
                try:
                    repayments = loan_repayment_service.list_repayments_for_loan(loan_id)
                    st.dataframe(repayments)
                    with st.expander("Make Repayment"):
                        with st.form("make_repayment"):
                            amount = st.number_input("Amount", min_value=0.01, format="%.2f")
                            submit = st.form_submit_button("Repay")
                            if submit:
                                try:
                                    loan_repayment_service.make_repayment(loan_id, amount)
                                    st.success("Repayment successful!")
                                except LoanRepaymentServiceError as e:
                                    st.error(f"Repayment failed: {e}")
                except LoanRepaymentServiceError as e:
                    st.error(f"Failed to load repayments: {e}")

    elif menu == "Employees":
        st.header("Employees")
        employees = load_employees()
        st.dataframe(employees)
        with st.expander("Add Employee"):
            with st.form("add_employee"):
                name = st.text_input("Name")
                role = st.text_input("Role")
                email = st.text_input("Email")
                phone = st.text_input("Phone")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Add")
                if submit:
                    try:
                        employee_service.add_employee(name, role, email, phone or None, password)
                        st.success("Employee added successfully!")
                    except EmployeeServiceError as e:
                        st.error(f"Failed to add employee: {e}")


if __name__ == "__main__":
    main()
