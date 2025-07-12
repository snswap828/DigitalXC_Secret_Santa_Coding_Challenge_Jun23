import pytest
from services.parser import Employee
from services.santa_assigner import SecretSantaAssigner

class TestSecretSantaAssigner:
    def test_assign_secret_children_basic(self):
        # Create test employees
        employees = [
            Employee("Alice", "alice@test.com"),
            Employee("Bob", "bob@test.com"),
            Employee("Charlie", "charlie@test.com")
        ]
        
        assigner = SecretSantaAssigner(employees, {})
        result = assigner.assign_secret_children()
        
        # Assertions
        assert len(result) == 3
        # Each employee should have a secret child
        for employee in result:
            assert employee.secret_child is not None
            assert employee.secret_child != employee  # Not assigned to themselves
        
        # All employees should be assigned as secret children
        assigned_children = [emp.secret_child for emp in result]
        assert len(set(assigned_children)) == 3  # All unique assignments

    def test_assign_with_previous_assignments(self):
        employees = [
            Employee("Alice", "alice@test.com"),
            Employee("Bob", "bob@test.com"),
            Employee("Charlie", "charlie@test.com"),
            Employee("David", "david@test.com")
        ]
        
        # Alice was previously assigned Bob
        previous_assignments = {
            "Alice": ["Bob"]
        }
        
        assigner = SecretSantaAssigner(employees, previous_assignments)
        result = assigner.assign_secret_children()
        
        # Find Alice in results
        alice = next(emp for emp in result if emp.name == "Alice")
        
        # Alice should not be assigned Bob again
        assert alice.secret_child.name != "Bob"
        assert alice.secret_child.name != "Alice"  # Not herself