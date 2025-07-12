import pandas as pd

class Employee:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.secret_child = None

class EmployeeParser:
    @staticmethod
    def parse(file_path):
        df = pd.read_excel(file_path)
        employees = []
        for _, row in df.iterrows():
            employee = Employee(
                name=row['Employee_Name'],
                email=row['Employee_EmailID']
            )
            employees.append(employee)
        return employees

class PreviousAssignmentParser:
    @staticmethod
    def parse(file_path):
        df = pd.read_excel(file_path)
        previous_assignments = {}
        for _, row in df.iterrows():
            employee_name = row['Employee_Name']
            secret_child_name = row['Secret_Child_Name']
            if employee_name not in previous_assignments:
                previous_assignments[employee_name] = []
            previous_assignments[employee_name].append(secret_child_name)
        return previous_assignments
