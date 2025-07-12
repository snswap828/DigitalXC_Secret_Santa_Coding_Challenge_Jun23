import random

class SecretSantaAssigner:
    def __init__(self, employees, previous_assignments=None):
        self.employees = employees
        self.previous_assignments = previous_assignments or {}
    
    def assign_secret_children(self):
        """Assign secret children to employees avoiding previous assignments"""
        # Create a copy of employees for available children
        available_children = self.employees.copy()
        
        for employee in self.employees:
            # Get list of people this employee was previously assigned
            previous_children = self.previous_assignments.get(employee.name, [])
            
            # Filter out invalid assignments: self and previous assignments
            valid_children = [
                child for child in available_children 
                if child.name != employee.name and child.name not in previous_children
            ]
            
            # If no valid children available, fall back to any available child except self
            if not valid_children:
                valid_children = [
                    child for child in available_children 
                    if child.name != employee.name
                ]
            
            if valid_children:
                secret_child = random.choice(valid_children)
                employee.secret_child = secret_child
                available_children.remove(secret_child)
        
        return self.employees
