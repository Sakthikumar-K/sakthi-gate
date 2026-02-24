#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garments.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from gate.models import Employee, SalaryStructure, Department

print('=' * 60)
print('DATABASE SUMMARY')
print('=' * 60)
print(f'Total Employees: {Employee.objects.count()}')
print(f'Total Salary Structures: {SalaryStructure.objects.count()}')
print(f'Total Departments: {Department.objects.count()}')
print('')
print(f'Active Employees: {Employee.objects.filter(status="A").count()}')
print(f'Inactive Employees: {Employee.objects.filter(status="I").count()}')
print(f'Suspended Employees: {Employee.objects.filter(status="S").count()}')
print('')
print('=' * 60)
print('SAMPLE OF LATEST ADDED EMPLOYEES')
print('=' * 60)
for emp in Employee.objects.all().order_by('-id')[:10]:
    salary = emp.salary_structure
    print(f'{emp.employee_id} | {emp.full_name:25} | {emp.designation:20} | {emp.department.name:15} | Salary: {salary.basic_salary}')
