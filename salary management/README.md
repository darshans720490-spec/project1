# Employee Salary Management System

A complete web-based employee salary management system with salary slip generation built using Python Flask, HTML, CSS, JavaScript, and SQLite.

## Features

- **Employee Management**: Add, view, and manage employee information
- **Salary Slip Generation**: Create professional salary slips with detailed breakdown
- **Database Storage**: SQLite database for persistent data storage
- **Responsive Design**: Mobile-friendly interface
- **Print Functionality**: Print salary slips directly from browser

## Technologies Used

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite
- **Styling**: Custom CSS with responsive design

## Installation & Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Database Schema

### Employees Table
- id (Primary Key)
- name
- email
- position
- department
- basic_salary
- allowances
- deductions
- created_at

### Salary Slips Table
- id (Primary Key)
- employee_id (Foreign Key)
- month
- year
- basic_salary
- allowances
- deductions
- gross_salary
- net_salary
- created_at

## Usage

1. **Add Employees**: Navigate to "Add Employee" to register new employees
2. **View Employees**: See all employees in the system with their basic information
3. **Generate Salary Slips**: Click "Generate Slip" for any employee to create their salary slip
4. **View Salary Slips**: Access all generated salary slips from the "Salary Slips" section
5. **Print Slips**: Use the print button on any salary slip for physical copies

## File Structure

```
salary management/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── salary_management.db   # SQLite database (auto-created)
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── employees.html
│   ├── add_employee.html
│   ├── generate_slip.html
│   ├── salary_slip.html
│   └── salary_slips.html
└── static/              # Static files
    ├── css/
    │   └── style.css    # Main stylesheet
    └── js/
        └── script.js    # JavaScript functionality
```