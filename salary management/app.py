from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

def number_to_words(n):
    if n == 0:
        return "Zero"
    
    ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
            "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
            "Seventeen", "Eighteen", "Nineteen"]
    
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    
    def convert_hundreds(num):
        result = ""
        if num >= 100:
            result += ones[num // 100] + " Hundred "
            num %= 100
        if num >= 20:
            result += tens[num // 10] + " "
            num %= 10
        if num > 0:
            result += ones[num] + " "
        return result
    
    if n < 0:
        return "Negative " + number_to_words(-n)
    
    if n < 20:
        return ones[n]
    elif n < 100:
        return tens[n // 10] + (" " + ones[n % 10] if n % 10 != 0 else "")
    elif n < 1000:
        return convert_hundreds(n).strip()
    elif n < 100000:
        return convert_hundreds(n // 1000) + "Thousand " + convert_hundreds(n % 1000)
    elif n < 10000000:
        return convert_hundreds(n // 100000) + "Lakh " + convert_hundreds((n % 100000) // 1000) + ("Thousand " if (n % 100000) // 1000 > 0 else "") + convert_hundreds(n % 1000)
    else:
        return convert_hundreds(n // 10000000) + "Crore " + convert_hundreds((n % 10000000) // 100000) + ("Lakh " if (n % 10000000) // 100000 > 0 else "") + convert_hundreds(((n % 10000000) % 100000) // 1000) + ("Thousand " if ((n % 10000000) % 100000) // 1000 > 0 else "") + convert_hundreds(n % 1000)

app.jinja_env.filters['number_to_words'] = number_to_words

def init_db():
    conn = sqlite3.connect('salary_management.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            position TEXT NOT NULL,
            department TEXT NOT NULL,
            basic_salary REAL NOT NULL,
            allowances REAL DEFAULT 0,
            deductions REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS salary_slips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            month TEXT NOT NULL,
            year INTEGER NOT NULL,
            basic_salary REAL NOT NULL,
            allowances REAL DEFAULT 0,
            deductions REAL DEFAULT 0,
            gross_salary REAL NOT NULL,
            net_salary REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (employee_id) REFERENCES employees (id)
        )
    ''')
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/employees')
def employees():
    conn = sqlite3.connect('salary_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees ORDER BY name')
    employees = cursor.fetchall()
    conn.close()
    return render_template('employees.html', employees=employees)

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        position = request.form['position']
        department = request.form['department']
        basic_salary = float(request.form['basic_salary'])
        allowances = float(request.form.get('allowances', 0))
        deductions = float(request.form.get('deductions', 0))
        
        conn = sqlite3.connect('salary_management.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO employees (name, email, position, department, basic_salary, allowances, deductions)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, email, position, department, basic_salary, allowances, deductions))
        conn.commit()
        conn.close()
        
        return redirect(url_for('employees'))
    
    return render_template('add_employee.html')

@app.route('/generate_slip/<int:employee_id>')
def generate_slip(employee_id):
    conn = sqlite3.connect('salary_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees WHERE id = ?', (employee_id,))
    employee = cursor.fetchone()
    conn.close()
    
    if not employee:
        return "Employee not found", 404
    
    return render_template('generate_slip.html', employee=employee)

@app.route('/create_slip', methods=['POST'])
def create_slip():
    employee_id = int(request.form['employee_id'])
    month = request.form['month']
    year = int(request.form['year'])
    basic_salary = float(request.form['basic_salary'])
    allowances = float(request.form.get('allowances', 0))
    deductions = float(request.form.get('deductions', 0))
    
    gross_salary = basic_salary + allowances
    net_salary = gross_salary - deductions
    
    conn = sqlite3.connect('salary_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO salary_slips (employee_id, month, year, basic_salary, allowances, deductions, gross_salary, net_salary)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (employee_id, month, year, basic_salary, allowances, deductions, gross_salary, net_salary))
    slip_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return redirect(url_for('view_slip', slip_id=slip_id))

@app.route('/view_slip/<int:slip_id>')
def view_slip(slip_id):
    conn = sqlite3.connect('salary_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.*, e.name, e.email, e.position, e.department
        FROM salary_slips s
        JOIN employees e ON s.employee_id = e.id
        WHERE s.id = ?
    ''', (slip_id,))
    slip_data = cursor.fetchone()
    conn.close()
    
    if not slip_data:
        return "Salary slip not found", 404
    
    return render_template('salary_slip.html', slip=slip_data)

@app.route('/delete_employee/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    conn = sqlite3.connect('salary_management.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM employees WHERE id = ?', (employee_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('employees'))

@app.route('/delete_slip/<int:slip_id>', methods=['POST'])
def delete_slip(slip_id):
    conn = sqlite3.connect('salary_management.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM salary_slips WHERE id = ?', (slip_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('salary_slips'))

@app.route('/salary_slips')
def salary_slips():
    conn = sqlite3.connect('salary_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.*, e.name
        FROM salary_slips s
        JOIN employees e ON s.employee_id = e.id
        ORDER BY s.created_at DESC
    ''')
    slips = cursor.fetchall()
    conn.close()
    return render_template('salary_slips.html', slips=slips)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)