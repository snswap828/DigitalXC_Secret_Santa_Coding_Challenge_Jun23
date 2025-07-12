import pytest
import sys
import os
import tempfile
import pandas as pd
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Import after path setup
from app import app
from services.parser import Employee

@pytest.fixture(scope="session")
def test_app():
    """Create application for the tests."""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    return app

@pytest.fixture
def client(test_app):
    """Create a test client for the Flask application."""
    return test_app.test_client()

@pytest.fixture
def sample_employees():
    """Create sample employee objects for testing."""
    return [
        Employee("Alice Johnson", "alice@company.com"),
        Employee("Bob Smith", "bob@company.com"),
        Employee("Charlie Brown", "charlie@company.com"),
        Employee("Diana Prince", "diana@company.com"),
        Employee("Eve Wilson", "eve@company.com")
    ]

@pytest.fixture
def sample_employee_excel():
    """Create a temporary Excel file with employee data."""
    data = {
        'Employee_Name': ['Alice Johnson', 'Bob Smith', 'Charlie Brown', 'Diana Prince', 'Eve Wilson'],
        'Employee_EmailID': ['alice@company.com', 'bob@company.com', 'charlie@company.com', 
                           'diana@company.com', 'eve@company.com']
    }
    df = pd.DataFrame(data)
    
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        df.to_excel(tmp.name, index=False)
        yield tmp.name
        os.unlink(tmp.name)

@pytest.fixture
def sample_previous_excel():
    """Create a temporary Excel file with previous assignment data."""
    data = {
        'Employee_Name': ['Alice Johnson', 'Bob Smith', 'Charlie Brown'],
        'Secret_Child_Name': ['Bob Smith', 'Diana Prince', 'Eve Wilson']
    }
    df = pd.DataFrame(data)
    
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        df.to_excel(tmp.name, index=False)
        yield tmp.name
        os.unlink(tmp.name)

@pytest.fixture
def empty_previous_excel():
    """Create an empty previous assignments file for new Secret Santa events."""
    data = {
        'Employee_Name': [],
        'Secret_Child_Name': []
    }
    df = pd.DataFrame(data)
    
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        df.to_excel(tmp.name, index=False)
        yield tmp.name
        os.unlink(tmp.name)