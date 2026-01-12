#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garments.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.contrib.auth.models import User
from gate.models import Employee, Department, SalaryStructure
from datetime import datetime

print("=" * 60)
print("Gate Garments - Demo Data Setup")
print("=" * 60)

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@gategarments.com', 'admin')
    print("✓ Superuser 'admin' created")
else:
    print("✓ Superuser 'admin' already exists")

# Create departments
dept1, created = Department.objects.get_or_create(
    name='Production',
    defaults={'description': 'Production Department'}
)
print(f"✓ Department 'Production' {'created' if created else 'exists'}")

dept2, created = Department.objects.get_or_create(
    name='Management',
    defaults={'description': 'Management & Administration'}
)
print(f"✓ Department 'Management' {'created' if created else 'exists'}")

dept3, created = Department.objects.get_or_create(
    name='Finance',
    defaults={'description': 'Finance Department'}
)
print(f"✓ Department 'Finance' {'created' if created else 'exists'}")

# Create demo employee user
if not User.objects.filter(username='emp001').exists():
    emp_user = User.objects.create_user('emp001', 'emp001@gategarments.com', 'emp001')
    emp_user.first_name = 'John'
    emp_user.last_name = 'Doe'
    emp_user.save()
    print("✓ User 'emp001' created")
else:
    emp_user = User.objects.get(username='emp001')
    print("✓ User 'emp001' already exists")

# Create employee profile
if not Employee.objects.filter(employee_id='EMP001').exists():
    emp = Employee.objects.create(
        employee_id='EMP001',
        user=emp_user,
        first_name='John',
        last_name='Doe',
        email='john.doe@gategarments.com',
        phone='9876543210',
        date_of_birth=datetime(1990, 5, 15).date(),
        gender='M',
        department=dept1,
        designation='Production Supervisor',
        date_of_joining=datetime(2023, 1, 1).date(),
        status='A',
        address='123 Main Street',
        city='Chennai',
        state='Tamil Nadu',
        postal_code='600001',
        bank_name='HDFC Bank',
        account_number='1234567890',
        ifsc_code='HDFC0001234'
    )
    print("✓ Employee 'EMP001' created")
    
    # Create salary structure for this employee
    SalaryStructure.objects.create(
        employee=emp,
        basic_salary=25000,
        hra=5000,
        dearness_allowance=3000,
        conveyance=1500,
        medical_allowance=1000,
        pf_contribution=2250,
        esi_contribution=800,
        income_tax=2000
    )
    print("✓ Salary structure for EMP001 created")
else:
    print("✓ Employee 'EMP001' already exists")

# Create another demo employee
if not User.objects.filter(username='emp002').exists():
    emp_user2 = User.objects.create_user('emp002', 'emp002@gategarments.com', 'emp002')
    emp_user2.first_name = 'Sarah'
    emp_user2.last_name = 'Johnson'
    emp_user2.save()
    print("✓ User 'emp002' created")
else:
    emp_user2 = User.objects.get(username='emp002')
    print("✓ User 'emp002' already exists")

if not Employee.objects.filter(employee_id='EMP002').exists():
    emp2 = Employee.objects.create(
        employee_id='EMP002',
        user=emp_user2,
        first_name='Sarah',
        last_name='Johnson',
        email='sarah.johnson@gategarments.com',
        phone='9876543211',
        date_of_birth=datetime(1992, 3, 20).date(),
        gender='F',
        department=dept2,
        designation='Finance Officer',
        date_of_joining=datetime(2023, 6, 15).date(),
        status='A',
        address='456 Park Avenue',
        city='Bangalore',
        state='Karnataka',
        postal_code='560001',
        bank_name='ICICI Bank',
        account_number='0987654321',
        ifsc_code='ICIC0000123'
    )
    print("✓ Employee 'EMP002' created")
    
    # Create salary structure
    SalaryStructure.objects.create(
        employee=emp2,
        basic_salary=30000,
        hra=6000,
        dearness_allowance=4000,
        conveyance=2000,
        medical_allowance=1500,
        pf_contribution=2700,
        esi_contribution=0,
        income_tax=3000
    )
    print("✓ Salary structure for EMP002 created")
else:
    print("✓ Employee 'EMP002' already exists")

print("\n" + "=" * 60)
print("✓ Demo setup complete!")
print("=" * 60)
print("\nLogin Credentials:")
print("  Admin: admin / admin")
print("  Employee 1: emp001 / emp001")
print("  Employee 2: emp002 / emp002")
print("\nAccess the system at: http://localhost:8000")
print("=" * 60)
