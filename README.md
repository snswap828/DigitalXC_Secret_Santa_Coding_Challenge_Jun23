# 🎁 DigitalXC Secret Santa Coding Challenge

A full-stack web application for generating Secret Santa assignments with intelligent pairing algorithms that avoid previous year assignments.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [API Documentation](#api-documentation)
- [Usage](#usage)


## ✨ Features

- 📊 **Excel File Upload**: Upload employee data and previous assignments via Excel files
- 🎯 **Smart Assignment Algorithm**: Avoids assigning same pairs from previous years
- 📈 **Real-time Processing**: Instant assignment generation with progress feedback
- 📄 **CSV Export**: Download results as CSV file for easy distribution
- 🔒 **Input Validation**: Robust error handling and file format validation
- 🎨 **Modern UI**: Clean, responsive interface built with Next.js and Tailwind CSS
- 🧪 **Comprehensive Testing**: Full test suite with 80%+ code coverage

## 🚀 Tech Stack

### Backend
- **Flask** - Python web framework
- **Pandas** - Excel file processing and data manipulation
- **OpenPyXL** - Excel file reading/writing
- **Flask-CORS** - Cross-origin resource sharing
- **Pytest** - Testing framework

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **React Hook Form** - Form handling
- **Zod** - Schema validation
- **Tanstack Query** - Data fetching and caching

## 📁 Project Structure

```
DigitalXC_Secret_Santa_Coding_Challenge/
├── backend/
│   ├── app.py                 # Flask application entry point
│   ├── services/
│   │   ├── __init__.py
│   │   ├── parser.py          # Excel file parsing logic
│   │   └── santa_assigner.py  # Secret Santa assignment algorithm
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py        # Pytest configuration and fixtures
│   │   ├── test_parser.py     # Parser unit tests
│   │   ├── test_santa_assigner.py # Assignment algorithm tests
│   │   ├── test_app.py        # API endpoint tests
│   │   └── test_integration.py # Integration tests
│   ├── requirements.txt       # Python dependencies
│   ├── test_requirements.txt  # Test dependencies
│   ├── pytest.ini            # Pytest configuration
│   └── Makefile              # Test automation commands
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js App Router pages
│   │   ├── components/       # Reusable UI components
│   │   ├── features/         # Feature-specific components
│   │   └── lib/             # Utilities and types
│   ├── package.json
│   └── tailwind.config.js
├── sample_data/
│   ├── employees.xlsx        # Sample employee data
│   └── previous_assignments.xlsx # Sample previous assignments
└── README.md
```

## 📋 Prerequisites

- **Python** 3.8 or higher
- **Node.js** 18 or higher
- **pnpm** or **yarn** package manager
- **Git** for version control

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/DigitalXC_Secret_Santa_Coding_Challenge.git
cd DigitalXC_Secret_Santa_Coding_Challenge
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install test dependencies (optional)
pip install -r test_requirements.txt
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
pnpm install


```

## ⚙️ Configuration

### Backend Configuration

The Flask backend runs on `http://localhost:5000` by default. No additional configuration is required for basic usage.

#### Environment Variables (Optional)

Create a `.env` file in the backend directory for custom configuration:

```bash
# backend/.env
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
```

### Frontend Configuration

The Next.js frontend runs on `http://localhost:3000` by default.

#### API Configuration

Update the API endpoint in `frontend/src/api/api.ts` if needed:

```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';
```

### File Format Requirements

#### Employee File (Excel)
Required columns:
- `Employee_Name`: Full name of employee
- `Employee_EmailID`: Email address

#### Previous Assignments File (Excel)
Required columns:
- `Employee_Name`: Full name of employee
- `Employee_EmailID`: Email address
- `Secret_Child_Name`: Name of previously assigned person
- `Secret_Child_EmailID`: Email of previously assigned person

## 🚀 Running the Application

### Development Mode

#### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate  # Activate virtual environment
python app.py
```

Backend will be available at: `http://localhost:5000`

#### Terminal 2 - Frontend
```bash
cd frontend
pnpm run dev
```

Frontend will be available at: `http://localhost:3000`


## 🧪 Testing

### Backend Testing

```bash
cd backend
source venv/bin/activate

# Run all tests
pytest

# Run with coverage
pytest --cov=services --cov=app --cov-report=html

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m api           # API tests only

# Run specific test files
pytest tests/test_parser.py -v
pytest tests/test_app.py -v

# Using Make commands
make test               # Run all tests
make test-coverage      # Run with coverage report
make test-unit          # Run unit tests only
```


### Test Coverage

Maintain minimum 80% test coverage. Coverage reports are generated in:
- Backend: `backend/htmlcov/index.html`
- Frontend: `frontend/coverage/lcov-report/index.html`

## 📚 API Documentation

### POST `/api/assign`

Generate Secret Santa assignments.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Files:
  - `employee`: Excel file with employee data
  - `previous`: Excel file with previous assignments

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "Employee_Name": "Alice Johnson",
      "Employee_EmailID": "alice@company.com",
      "Secret_Child_Name": "Bob Smith",
      "Secret_Child_EmailID": "bob@company.com"
    }
  ]
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error message description"
}
```

## 📖 Usage

### Step 1: Prepare Excel Files

1. **Employee File**: Create an Excel file with employee names and emails
2. **Previous Assignments**: Create an Excel file with previous year assignments (can be empty for first year)

### Step 2: Upload and Generate

1. Open the application at `http://localhost:3000`
2. Upload both Excel files using the file upload interface
3. Click "Generate Assignments" button
4. Wait for processing to complete

### Step 3: Download Results

1. Download the generated xlsx file
2. Distribute assignments to employees
3. Save the xlsx file as next year's "previous assignments" input

### Sample Data

Sample Excel files are provided in the `sample_data/` directory for testing:
- `employees.xlsx`: Sample employee data
- `previous_assignments.xlsx`: Sample previous assignments

### Code Standards

- **Python**: Follow PEP 8 style guidelines
- **TypeScript**: Use ESLint and Prettier configurations
- **Tests**: Maintain 80%+ coverage
- **Commits**: Use conventional commit messages



### Common Issues

#### Backend Issues

**Error: "No module named 'services'"**
```bash
# Ensure you're in the backend directory and virtual environment is activated
cd backend
source venv/bin/activate
python app.py
```

**Error: "ModuleNotFoundError: No module named 'openpyxl'"**
```bash
# Install missing dependencies
pip install -r requirements.txt
```

**Error: "CORS Missing Allow Origin"**
- Ensure Flask-CORS is installed: `pip install flask-cors`
- Check that CORS is enabled in `app.py`

#### Frontend Issues

**Error: "Module not found"**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
pnpm install
```

**Error: "Port 3000 is already in use"**
```bash
# Use different port
pnpm run dev -- -p 3001
```

#### File Upload Issues

**Error: "Invalid file format"**
- Ensure Excel files have `.xlsx` extension
- Check that required columns exist with correct names
- Verify files are not corrupted

**Error: "Assignment algorithm failed"**
- Ensure at least 2 employees in the file
- Check for duplicate employee names
- Verify previous assignments reference valid employee names
