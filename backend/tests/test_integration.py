import pytest
import tempfile
import pandas as pd
import os
from services.parser import EmployeeParser, PreviousAssignmentParser
from services.santa_assigner import SecretSantaAssigner

class TestIntegration:
    def test_full_secret_santa_workflow(self):
        # Create employee data
        employee_data = {
            'Employee_Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'Employee_EmailID': ['alice@test.com', 'bob@test.com', 'charlie@test.com', 
                               'david@test.com', 'eve@test.com']
        }
        employee_df = pd.DataFrame(employee_data)
        
        # Create previous assignment data
        previous_data = {
            'Employee_Name': ['Alice', 'Bob'],
            'Secret_Child_Name': ['Bob', 'Charlie']
        }
        previous_df = pd.DataFrame(previous_data)
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as emp_tmp, \
             tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as prev_tmp:
            
            employee_df.to_excel(emp_tmp.name, index=False)
            previous_df.to_excel(prev_tmp.name, index=False)
            
            try:
                # Parse files
                employees = EmployeeParser.parse(emp_tmp.name)
                previous_assignments = PreviousAssignmentParser.parse(prev_tmp.name)
                
                # Assign secret children
                assigner = SecretSantaAssigner(employees, previous_assignments)
                result = assigner.assign_secret_children()
                
                # Verify results
                assert len(result) == 5
                
                # Check that previous assignments are respected
                alice = next(emp for emp in result if emp.name == "Alice")
                bob = next(emp for emp in result if emp.name == "Bob")
                
                # Alice should not get Bob (previous assignment)
                assert alice.secret_child.name != "Bob"
                # Bob should not get Charlie (previous assignment)
                assert bob.secret_child.name != "Charlie"
                
                # No one should be assigned to themselves
                for employee in result:
                    assert employee.secret_child.name != employee.name
                
                # All assignments should be unique
                assigned_names = [emp.secret_child.name for emp in result]
                assert len(set(assigned_names)) == len(assigned_names)
                
            finally:
                # Cleanup
                os.unlink(emp_tmp.name)
                os.unlink(prev_tmp.name)