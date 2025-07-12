import pytest
import tempfile
import pandas as pd
import os
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_employee_file():
    data = {
        'Employee_Name': ['Alice', 'Bob', 'Charlie'],
        'Employee_EmailID': ['alice@test.com', 'bob@test.com', 'charlie@test.com']
    }
    df = pd.DataFrame(data)
    
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        df.to_excel(tmp.name, index=False)
        yield tmp.name
        os.unlink(tmp.name)

@pytest.fixture
def sample_previous_file():
    data = {
        'Employee_Name': ['Alice'],
        'Secret_Child_Name': ['Bob']
    }
    df = pd.DataFrame(data)
    
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        df.to_excel(tmp.name, index=False)
        yield tmp.name
        os.unlink(tmp.name)

class TestFlaskAPI:
    def test_assign_santa_success(self, client, sample_employee_file, sample_previous_file):
        with open(sample_employee_file, 'rb') as emp_file, \
             open(sample_previous_file, 'rb') as prev_file:
            
            response = client.post('/api/assign', data={
                'employee': (emp_file, 'employees.xlsx'),
                'previous': (prev_file, 'previous.xlsx')
            }, content_type='multipart/form-data')
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['success'] is True
            assert 'data' in data
            assert len(data['data']) == 3

    def test_assign_santa_missing_employee_file(self, client, sample_previous_file):
        with open(sample_previous_file, 'rb') as prev_file:
            response = client.post('/api/assign', data={
                'previous': (prev_file, 'previous.xlsx')
            }, content_type='multipart/form-data')
            
            assert response.status_code == 400
            data = response.get_json()
            assert data['success'] is False
            assert 'No employee file provided' in data['error']

    def test_assign_santa_missing_previous_file(self, client, sample_employee_file):
        with open(sample_employee_file, 'rb') as emp_file:
            response = client.post('/api/assign', data={
                'employee': (emp_file, 'employees.xlsx')
            }, content_type='multipart/form-data')
            
            assert response.status_code == 400
            data = response.get_json()
            assert data['success'] is False
            assert 'No previous assignment file provided' in data['error']