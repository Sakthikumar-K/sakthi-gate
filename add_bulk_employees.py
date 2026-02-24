#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garments.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.contrib.auth.models import User
from gate.models import Employee, Department, SalaryStructure

print("=" * 70)
print("Bulk Employee Data Setup - Adding 400 Employees")
print("=" * 70)

# Get or create departments
departments = []
dept_names = ['Production', 'Management', 'Finance', 'HR', 'Quality Assurance', 'Packaging', 'Logistics']

for dept_name in dept_names:
    dept, created = Department.objects.get_or_create(
        name=dept_name,
        defaults={'description': f'{dept_name} Department'}
    )
    departments.append(dept)
    status = 'created' if created else 'exists'
    print(f"[OK] Department '{dept_name}' {status}")

# First names and last names for realistic employee data
first_names = ['Raj', 'Priya', 'Arun', 'Deepa', 'Vijay', 'Anita', 'Suresh', 'Meera', 
               'Arjun', 'Shalini', 'Manish', 'Kavya', 'Ramesh', 'Divya', 'Akshay', 'Neha',
               'Sandeep', 'Anjali', 'Naveen', 'Pooja', 'Ashok', 'Sneha', 'Karthik', 'Swati',
               'Harish', 'Isha', 'Vikram', 'Shreya', 'Nikhil', 'Ankita', 'Rahul', 'Ritika',
               'Tanmay', 'Aditi', 'Varun', 'Disha', 'Sanjay', 'Sakshi', 'Harsh', 'Shruti',
               'Rohan', 'Nikita', 'Sameer', 'Viya', 'Hemant', 'Megha', 'Abhishek', 'Nitya']

last_names = ['Kumar', 'Singh', 'Sharma', 'Patel', 'Reddy', 'Verma', 'Pandey', 'Desai',
              'Gupta', 'Joshi', 'Nair', 'Iyer', 'Mishra', 'Tripathi', 'Sinha', 'Chakraborty',
              'Mahajan', 'Agarwal', 'Kulkarni', 'Rao', 'Pillai', 'Subramanian', 'Yadav', 'Mukherjee',
              'Banerjee', 'Chatterjee', 'Dutta', 'Ghosh', 'Bhat', 'Menon', 'Das', 'Roy',
              'Saxena', 'Tiwari', 'Shukla', 'Awasthi', 'Behl', 'Malhotra', 'Sethi', 'Dhawan']

designations = [
    'Production Supervisor', 'Machine Operator', 'Quality Inspector', 'Packing Staff',
    'Floor Manager', 'Assembly Technician', 'Welder', 'Cutter', 'Stitcher', 'Presser',
    'Manager', 'Assistant Manager', 'Team Lead', 'Senior Executive', 'Junior Executive',
    'Finance Officer', 'Accountant', 'HR Officer', 'Recruiter', 'Admin Executive',
    'Logistics Coordinator', 'Driver', 'Store Keeper', 'Quality Analyst', 'Chemist'
]

# Cities in India
cities = ['Chennai', 'Bangalore', 'Hyderabad', 'Delhi', 'Mumbai', 'Pune', 'Kolkata', 
          'Coimbatore', 'Madurai', 'Tiruppur', 'Salem', 'Vellore', 'Kanchipuram', 'Erode']

states = ['Tamil Nadu', 'Karnataka', 'Telangana', 'Delhi', 'Maharashtra', 'West Bengal',
          'Andhra Pradesh', 'Kerala', 'Gujarat', 'Rajasthan', 'Uttar Pradesh', 'Punjab']

# Bank details
bank_names = ['HDFC Bank', 'ICICI Bank', 'SBI Bank', 'Axis Bank', 'Kotak Bank', 
              'IndusInd Bank', 'Federal Bank', 'Yes Bank', 'IDBI Bank', 'Union Bank']

print("\nGenerating 400 employees...")
print("-" * 70)

# Generate employee data
employees_to_create = []
users_data = []
salary_structures_to_create = []

start_date = datetime(2020, 1, 1)
base_date = datetime(1985, 1, 1)

existing_count = Employee.objects.count()
existing_users = User.objects.filter(username__startswith='emp').count()

for i in range(1, 401):
    emp_num = existing_count + i
    user_num = existing_users + i
    
    # Generate unique employee ID
    employee_id = f'EMP{emp_num:04d}'
    username = f'emp{user_num:05d}'
    
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    email = f'{username}@gategarments.com'
    
    # Random date of birth (age between 22-60)
    dob = base_date + timedelta(days=random.randint(0, 365*38))
    
    # Random joining date
    joining_date = start_date + timedelta(days=random.randint(0, (datetime(2024, 12, 31) - start_date).days))
    
    # Store user data for bulk creation
    users_data.append({
        'username': username,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'password': username
    })
    
    # Create Employee object
    employee = Employee(
        employee_id=employee_id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=f'98{random.randint(7654320000, 9999999999)}',
        date_of_birth=dob.date(),
        gender=random.choice(['M', 'F', 'O']),
        department=random.choice(departments),
        designation=random.choice(designations),
        date_of_joining=joining_date.date(),
        status=random.choice(['A', 'A', 'A', 'I', 'S']),  # 60% Active, 20% Inactive, 20% Suspended
        address=f'{random.randint(1, 999)} Main Street, Apartment {random.randint(1, 100)}',
        city=random.choice(cities),
        state=random.choice(states),
        postal_code=f'{random.randint(100000, 999999)}',
        bank_name=random.choice(bank_names),
        account_number=f'{random.randint(10000000000, 99999999999)}',
        ifsc_code=f'{random.choice(["HDFC", "ICIC", "SBIN", "UTIB", "INDB"])}{random.randint(0, 9)}{random.choice([chr(65+j) for j in range(26)])}'
    )
    employees_to_create.append(employee)
    
    # Create salary structure
    basic_salary = random.randint(15000, 50000)
    salary_structure = SalaryStructure(
        employee=employee,
        basic_salary=basic_salary,
        hra=int(basic_salary * 0.2),
        dearness_allowance=int(basic_salary * 0.1),
        conveyance=random.choice([1500, 2000, 2500]),
        medical_allowance=random.choice([1000, 1500, 2000]),
        other_allowances=random.randint(0, 5000),
        pf_contribution=int(basic_salary * 0.12),
        esi_contribution=int(basic_salary * 0.0475) if basic_salary < 21000 else 0,
        income_tax=int(basic_salary * 0.1)
    )
    salary_structures_to_create.append(salary_structure)
    
    if i % 100 == 0:
        print(f"  Prepared {i} employees...")

# Bulk create users first (without setting passwords yet to speed up)
print(f"\n[IN PROGRESS] Creating {len(users_data)} users in batch...")
created_users = []
for user_data in users_data:
    user = User.objects.create_user(
        username=user_data['username'],
        email=user_data['email'],
        password=user_data['password']
    )
    user.first_name = user_data['first_name']
    user.last_name = user_data['last_name']
    user.save(update_fields=['first_name', 'last_name'])
    created_users.append(user)
    
print(f"[OK] {len(created_users)} users created")

# Assign users to employees
for emp, user in zip(employees_to_create, created_users):
    emp.user = user

# Bulk create employees
print(f"[IN PROGRESS] Creating {len(employees_to_create)} employees in batch...")
created_employees = Employee.objects.bulk_create(employees_to_create, batch_size=100)
print(f"[OK] {len(created_employees)} employees created")

# Update salary structures with created employee references
for sal_struct, emp in zip(salary_structures_to_create, created_employees):
    sal_struct.employee = emp

# Bulk create salary structures
print(f"[IN PROGRESS] Creating {len(salary_structures_to_create)} salary structures in batch...")
SalaryStructure.objects.bulk_create(salary_structures_to_create, batch_size=100)
print(f"[OK] {len(salary_structures_to_create)} salary structures created")

print("\n" + "=" * 70)
print("[SUCCESS] BULK DATA SETUP COMPLETE!")
print("=" * 70)
print(f"\nSummary:")
print(f"   Total Employees in Database: {Employee.objects.count()}")
print(f"   Total Users: {User.objects.count()}")
print(f"   Total Salary Structures: {SalaryStructure.objects.count()}")
print(f"\n[OK] {len(employees_to_create)} new employees added successfully!")
print(f"[OK] Database is now fully populated with realistic data")
print("=" * 70)
print("\nSample Login Credentials:")
print("  Admin: admin / admin")
print("  Employees: emp00001 / emp00001, emp00002 / emp00002, etc.")
print("=" * 70)
