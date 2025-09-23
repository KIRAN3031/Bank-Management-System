import json
from src.services.bm_customer_service import CustomerService, CustomerServiceError
from src.services.bm_account_service import AccountService, AccountServiceError
from src.services.bm_transaction_service import TransactionService, TransactionServiceError
from src.services.bm_loan_service import LoanService, LoanServiceError
from src.services.bm_employee_service import EmployeeService, EmployeeServiceError
from src.services.bm_loan_repayment_service import LoanRepaymentService, LoanRepaymentServiceError

class BankMenu:
    def __init__(self):
        self.customer_service = CustomerService()
        self.account_service = AccountService()
        self.transaction_service = TransactionService()
        self.loan_service = LoanService()
        self.employee_service = EmployeeService()
        self.loan_repayment_service = LoanRepaymentService()
        self.running = True

    def print_menu(self):
        print("\nBank Management System Menu")
        print("1. Add Customer")
        print("2. List Customers")
        print("3. Open Account")
        print("4. Deposit")
        print("5. Withdraw")
        print("6. Transfer")
        print("7. Apply Loan")
        print("8. Repay Loan")
        print("9. List Loans")
        print("10. Add Employee")
        print("0. Exit")

    def run(self):
        while self.running:
            self.print_menu()
            choice = input("Enter your choice: ").strip()

            match choice:
                case "1":
                    self.add_customer()
                case "2":
                    self.list_customers()
                case "3":
                    self.open_account()
                case "4":
                    self.deposit()
                case "5":
                    self.withdraw()
                case "6":
                    self.transfer()
                case "7":
                    self.apply_loan()
                case "8":
                    self.repay_loan()
                case "9":
                    self.list_loans()
                case "10":
                    self.add_employee()
                case "0":
                    print("Exiting the program.")
                    self.running = False
                case _:
                    print("Invalid choice. Please enter a valid number from the menu.")

    # Implementations of each menu option below:
    def add_customer(self):
        try:
            name = input("Name: ")
            email = input("Email: ")
            phone = input("Phone (optional): ")
            city = input("City (optional): ")
            address = input("Address (optional): ")
            customer = self.customer_service.create_customer(name, email, phone or None, city or None, address or None)
            print("Customer created:", json.dumps(customer, indent=2))
        except CustomerServiceError as e:
            print("Error:", e)

    def list_customers(self):
        try:
            customers = self.customer_service.list_customers()
            print("Customers:", json.dumps(customers, indent=2))
        except CustomerServiceError as e:
            print("Error:", e)

    def open_account(self):
        try:
            cust_id = int(input("Customer ID: "))
            acc_type = input("Account Type (Savings/Checking): ")
            account = self.account_service.open_account(cust_id, acc_type)
            print("Account opened:", json.dumps(account, indent=2))
        except AccountServiceError as e:
            print("Error:", e)
        except ValueError:
            print("Please enter a valid Customer ID (integer)")

    def deposit(self):
        try:
            acc_id = int(input("Account ID: "))
            amount = float(input("Deposit Amount: "))
            txn = self.transaction_service.deposit(acc_id, amount)
            print("Deposit successful:", json.dumps(txn, indent=2))
        except TransactionServiceError as e:
            print("Error:", e)
        except ValueError:
            print("Invalid input for account ID or amount")

    def withdraw(self):
        try:
            acc_id = int(input("Account ID: "))
            amount = float(input("Withdraw Amount: "))
            txn = self.transaction_service.withdraw(acc_id, amount)
            print("Withdrawal successful:", json.dumps(txn, indent=2))
        except TransactionServiceError as e:
            print("Error:", e)
        except ValueError:
            print("Invalid input for account ID or amount")

    def transfer(self):
        try:
            from_acc = int(input("From Account ID: "))
            to_acc = int(input("To Account ID: "))
            amount = float(input("Transfer Amount: "))
            txn = self.transaction_service.transfer(from_acc, to_acc, amount)
            print("Transfer successful:", json.dumps(txn, indent=2))
        except TransactionServiceError as e:
            print("Error:", e)
        except ValueError:
            print("Invalid input for account IDs or amount")

    def apply_loan(self):
        try:
            cust_id = int(input("Customer ID: "))
            loan_type = input("Loan Type: ")
            amount = float(input("Loan Amount: "))
            interest_rate = float(input("Interest Rate: "))
            loan = self.loan_service.apply_for_loan(cust_id, loan_type, amount, interest_rate)
            print("Loan applied:", json.dumps(loan, indent=2))
        except LoanServiceError as e:
            print("Error:", e)
        except ValueError:
            print("Invalid input for customer ID, amount, or interest rate")

    def repay_loan(self):
        try:
            loan_id = int(input("Loan ID: "))
            amount = float(input("Repayment Amount: "))
            repayment = self.loan_repayment_service.make_repayment(loan_id, amount)
            print("Loan repayment successful:", json.dumps(repayment, indent=2))
        except LoanRepaymentServiceError as e:
            print("Error:", e)
        except ValueError:
            print("Invalid input for loan ID or amount")

    def list_loans(self):
        print("Listing all loans feature not yet implemented.")

    def add_employee(self):
        try:
            name = input("Employee Name: ")
            role = input("Role: ")
            email = input("Email: ")
            phone = input("Phone (optional): ")
            password = input("Password: ")
            emp = self.employee_service.add_employee(name, role, email, phone or None, password)
            print("Employee added:", json.dumps(emp, indent=2))
        except EmployeeServiceError as e:
            print("Error:", e)

def main():
    menu = BankMenu()
    menu.run()

if __name__ == "__main__":
    main()
