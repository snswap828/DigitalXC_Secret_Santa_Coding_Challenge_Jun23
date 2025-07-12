import pytest
import pandas as pd
import tempfile
import os
from services.parser import Employee, EmployeeParser, PreviousAssignmentParser

class TestEmployee:
    def test_employee_initialization(self):
        employee = Employee("John Doe", "john@example.com")
        assert employee.name == "John Doe"
        assert employee.email == "john@example.com"
        assert employee.secret_child is None

class TestEmployeeParser:
    def test_parse_valid_excel_file(self):
        # Create test data
        data = {
            'Employee_Name': ['Alice', 'Bob', 'Charlie'],
            'Employee_EmailID': ['alice@test.com', 'bob@test.com', 'charlie@test.com']
        }
        df = pd.DataFrame(data)
        
        # Create temporary Excel file
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            df.to_excel(tmp.name, index=False)
            
            # Parse the file
            employees = EmployeeParser.parse(tmp.name)
            
            # Assertions
            assert len(employees) == 3
            assert employees[0].name == 'Alice'
            assert employees[0].email == 'alice@test.com'
            assert employees[1].name == 'Bob'
            assert employees[2].name == 'Charlie'
            
            # Cleanup
            os.unlink(tmp.name)

class TestPreviousAssignmentParser:
    def test_parse_previous_assignments(self):
        # Create test data
        data = {
            'Employee_Name': ['Alice', 'Bob', 'Alice'],
            'Secret_Child_Name': ['Bob', 'Charlie', 'Charlie']
        }
        df = pd.DataFrame(data)
        
        # Create temporary Excel file
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            df.to_excel(tmp.name, index=False)
            
            # Parse the file
            previous = PreviousAssignmentParser.parse(tmp.name)
            
            # Assertions
            assert 'Alice' in previous
            assert 'Bob' in previous
            assert len(previous['Alice']) == 2
            assert 'Bob' in previous['Alice']
            assert 'Charlie' in previous['Alice']
            
            # Cleanup
            os.unlink(tmp.name)