from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Sum, Count
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from calendar import monthcalendar, month_name
import calendar

from .models import (
    Employee, Attendance, Leave, SalaryStructure, PayrollMonth, 
    PayrollRecord, SalarySlip, Department, Deduction, HolidayCalendar
)

# ============= DASHBOARD VIEWS =============

@login_required
def dashboard(request):
    """Main dashboard - role-based redirect"""
    try:
        employee = Employee.objects.get(user=request.user)
        return redirect('employee_dashboard')
    except Employee.DoesNotExist:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('employee_list')


@login_required
def employee_dashboard(request):
    """Employee's personal dashboard"""
    try:
        employee = Employee.objects.get(user=request.user)
        
        # Current month attendance
        today = datetime.now()
        current_month_start = today.replace(day=1)
        current_month_end = (current_month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        attendance_records = Attendance.objects.filter(
            employee=employee,
            date__range=[current_month_start, current_month_end]
        )
        
        # Attendance summary
        present_count = attendance_records.filter(status='P').count()
        absent_count = attendance_records.filter(status='A').count()
        leave_count = attendance_records.filter(status='L').count()
        
        # Recent payroll
        payroll_records = PayrollRecord.objects.filter(employee=employee).order_by('-payroll_month')[:3]
        
        # Pending leaves
        pending_leaves = Leave.objects.filter(employee=employee, status='P')
        
        context = {
            'employee': employee,
            'present_count': present_count,
            'absent_count': absent_count,
            'leave_count': leave_count,
            'total_attendance': attendance_records.count(),
            'payroll_records': payroll_records,
            'pending_leaves': pending_leaves,
        }
        return render(request, 'gate/employee_dashboard.html', context)
    except Employee.DoesNotExist:
        return redirect('admin_dashboard')


@login_required
def admin_dashboard(request):
    """Admin dashboard with statistics"""
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('employee_dashboard')
    
    total_employees = Employee.objects.filter(status='A').count()
    total_departments = Department.objects.count()
    
    # Today's attendance
    today = datetime.now().date()
    today_attendance = Attendance.objects.filter(date=today)
    present_today = today_attendance.filter(status='P').count()
    absent_today = today_attendance.filter(status='A').count()
    
    # Pending leaves
    pending_leaves = Leave.objects.filter(status='P').count()
    
    # Recent payrolls
    payroll_months = PayrollMonth.objects.order_by('-year', '-month')[:5]
    
    context = {
        'total_employees': total_employees,
        'total_departments': total_departments,
        'present_today': present_today,
        'absent_today': absent_today,
        'pending_leaves': pending_leaves,
        'payroll_months': payroll_months,
    }
    return render(request, 'gate/admin_dashboard.html', context)


# ============= EMPLOYEE MANAGEMENT =============

@login_required
def employee_list(request):
    """List all employees with filtering"""
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('employee_dashboard')
    
    employees = Employee.objects.select_related('department').all()
    
    # Filter by department
    department = request.GET.get('department')
    if department:
        employees = employees.filter(department_id=department)
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        employees = employees.filter(status=status)
    
    # Search
    search = request.GET.get('search')
    if search:
        employees = employees.filter(
            Q(employee_id__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    departments = Department.objects.all()
    context = {
        'employees': employees,
        'departments': departments,
    }
    return render(request, 'gate/employee_list.html', context)


@login_required
def employee_detail(request, employee_id):
    """Employee details view"""
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('employee_dashboard')
    
    employee = get_object_or_404(Employee, pk=employee_id)
    salary_structure = getattr(employee, 'salary_structure', None)
    
    context = {
        'employee': employee,
        'salary_structure': salary_structure,
    }
    return render(request, 'gate/employee_detail.html', context)


@login_required
def employee_edit(request, employee_id):
    """Edit employee details"""
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('employee_dashboard')
    
    employee = get_object_or_404(Employee, pk=employee_id)
    departments = Department.objects.all()
    
    if request.method == 'POST':
        try:
            # Update employee fields
            employee.first_name = request.POST.get('first_name')
            employee.last_name = request.POST.get('last_name')
            employee.email = request.POST.get('email')
            employee.phone = request.POST.get('phone', '')
            employee.date_of_birth = request.POST.get('date_of_birth')
            employee.gender = request.POST.get('gender')
            
            # Employment details
            department_id = request.POST.get('department')
            if department_id:
                employee.department_id = department_id
            
            employee.designation = request.POST.get('designation')
            employee.date_of_joining = request.POST.get('date_of_joining')
            employee.status = request.POST.get('status')
            
            # Contact information
            employee.address = request.POST.get('address')
            employee.city = request.POST.get('city')
            employee.state = request.POST.get('state')
            employee.postal_code = request.POST.get('postal_code')
            
            # Bank details
            employee.bank_name = request.POST.get('bank_name', '')
            employee.account_number = request.POST.get('account_number', '')
            employee.ifsc_code = request.POST.get('ifsc_code', '')
            
            # Save changes
            employee.save()
            
            from django.contrib import messages
            messages.success(request, f'Employee {employee.full_name} has been updated successfully!')
            
            return redirect('employee_detail', employee_id=employee.id)
        
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f'Error updating employee: {str(e)}')
    
    context = {
        'employee': employee,
        'form': {},
        'departments': departments,
    }
    return render(request, 'gate/employee_edit.html', context)


@login_required
def employee_add(request):
    """Add new employee"""
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('employee_dashboard')
    
    departments = Department.objects.all()
    
    if request.method == 'POST':
        try:
            # Generate unique employee ID
            from django.db.models import Max
            last_employee = Employee.objects.all().order_by('-id').first()
            employee_id = f"EMP{(last_employee.id if last_employee else 0) + 1:05d}"
            
            # Create new employee
            employee = Employee(
                employee_id=employee_id,
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone', ''),
                date_of_birth=request.POST.get('date_of_birth'),
                gender=request.POST.get('gender'),
                department_id=request.POST.get('department'),
                designation=request.POST.get('designation'),
                date_of_joining=request.POST.get('date_of_joining'),
                status=request.POST.get('status', 'A'),
                address=request.POST.get('address'),
                city=request.POST.get('city'),
                state=request.POST.get('state'),
                postal_code=request.POST.get('postal_code'),
                bank_name=request.POST.get('bank_name', ''),
                account_number=request.POST.get('account_number', ''),
                ifsc_code=request.POST.get('ifsc_code', ''),
            )
            
            employee.save()
            
            from django.contrib import messages
            messages.success(request, f'Employee {employee.full_name} has been created successfully!')
            
            return redirect('employee_detail', employee_id=employee.id)
        
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f'Error creating employee: {str(e)}')
    
    context = {
        'departments': departments,
        'is_new': True,
    }
    return render(request, 'gate/employee_add.html', context)


@login_required
def employee_delete(request, employee_id):
    """Delete employee"""
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('employee_dashboard')
    
    employee = get_object_or_404(Employee, pk=employee_id)
    
    try:
        employee_name = employee.full_name
        employee.delete()
        
        from django.contrib import messages
        messages.success(request, f'Employee {employee_name} has been deleted successfully!')
    except Exception as e:
        from django.contrib import messages
        messages.error(request, f'Error deleting employee: {str(e)}')
    
    return redirect('employee_list')


@login_required
def attendance_view(request):
    """Mark and view attendance"""
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('employee_dashboard')
    
    today = datetime.now().date()
    
    if request.method == 'POST':
        success_count = 0
        error_count = 0
        
        # Check if this is bulk submission (attendance[id]=status format)
        attendance_data = {}
        for key, value in request.POST.items():
            if key.startswith('attendance[') and key.endswith(']'):
                emp_id = key[11:-1]  # Extract employee_id from "attendance[id]"
                attendance_data[emp_id] = value
        
        # If no bulk data, try single submission (for backward compatibility)
        if not attendance_data:
            employee_id = request.POST.get('employee_id')
            status = request.POST.get('status')
            check_in_time = request.POST.get('check_in_time')
            check_out_time = request.POST.get('check_out_time')
            remarks = request.POST.get('remarks', '')
            
            if employee_id:
                try:
                    employee = Employee.objects.get(pk=employee_id)
                    attendance, created = Attendance.objects.update_or_create(
                        employee=employee,
                        date=today,
                        defaults={
                            'status': status,
                            'check_in_time': check_in_time or None,
                            'check_out_time': check_out_time or None,
                            'remarks': remarks,
                        }
                    )
                    success_count = 1
                except Employee.DoesNotExist:
                    error_count = 1
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Attendance marked'})
            return redirect('attendance_view')
        
        # Process bulk attendance submission
        for employee_id, status in attendance_data.items():
            try:
                employee = Employee.objects.get(pk=employee_id)
                attendance, created = Attendance.objects.update_or_create(
                    employee=employee,
                    date=today,
                    defaults={'status': status}
                )
                success_count += 1
            except Employee.DoesNotExist:
                error_count += 1
            except Exception as e:
                error_count += 1
        
        # Return JSON response for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if error_count == 0:
                return JsonResponse({'status': 'success', 'message': f'Attendance marked successfully for {success_count} employee(s)'})
            else:
                return JsonResponse({'status': 'partial', 'message': f'Marked {success_count} employee(s), {error_count} failed'}, status=400)
        
        return redirect('attendance_view')
    
    employees = Employee.objects.filter(status='A')
    today_attendance = Attendance.objects.filter(date=today)
    
    # Get IDs of employees marked as present
    marked_employees = list(today_attendance.filter(status='P').values_list('employee_id', flat=True))
    
    # Count attendance by status
    attendance_counts = {
        'P': today_attendance.filter(status='P').count(),
        'A': today_attendance.filter(status='A').count(),
        'L': today_attendance.filter(status='L').count(),
        'H': today_attendance.filter(status='H').count(),
    }
    
    context = {
        'employees': employees,
        'today': today,
        'today_attendance': today_attendance,
        'marked_employees': marked_employees,
        'attendance_counts': attendance_counts,
    }
    return render(request, 'gate/attendance.html', context)


@login_required
def attendance_report(request):
    """View attendance report for a range"""
    if not (request.user.is_staff or request.user.is_superuser):
        try:
            employee = Employee.objects.get(user=request.user)
            return attendance_report_employee(request, employee.id)
        except Employee.DoesNotExist:
            return redirect('employee_dashboard')
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    employee_filter = request.GET.get('employee')
    
    attendance_records = Attendance.objects.select_related('employee').all()
    
    if start_date:
        attendance_records = attendance_records.filter(date__gte=start_date)
    if end_date:
        attendance_records = attendance_records.filter(date__lte=end_date)
    if employee_filter:
        attendance_records = attendance_records.filter(employee_id=employee_filter)
    
    attendance_records = attendance_records.order_by('-date')
    
    employees = Employee.objects.filter(status='A')
    
    context = {
        'attendance_records': attendance_records,
        'employees': employees,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'gate/attendance_report.html', context)


# ============= LEAVE MANAGEMENT =============

@login_required
def leave_request(request):
    """Create new leave request"""
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        return redirect('login')
    
    if request.method == 'POST':
        leave_type = request.POST.get('leave_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')
        
        Leave.objects.create(
            employee=employee,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            status='P'
        )
        
        return redirect('leave_list')
    
    context = {
        'leave_types': Leave._meta.get_field('leave_type').choices,
    }
    return render(request, 'gate/leave_request.html', context)


@login_required
def leave_list(request):
    """View leaves"""
    try:
        employee = Employee.objects.get(user=request.user)
        leaves = employee.leaves.all().order_by('-start_date')
    except Employee.DoesNotExist:
        if not (request.user.is_staff or request.user.is_superuser):
            return redirect('login')
        leaves = Leave.objects.all().order_by('-start_date')
    
    context = {
        'leaves': leaves,
    }
    return render(request, 'gate/leave_list.html', context)


@login_required
def leave_approve(request, leave_id):
    """Approve or reject leave"""
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('leave_list')
    
    leave = get_object_or_404(Leave, pk=leave_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            leave.status = 'A'
        elif action == 'reject':
            leave.status = 'R'
        
        leave.approved_by = request.user
        leave.approval_date = datetime.now()
        leave.save()
        
        return redirect('leave_list')
    
    context = {
        'leave': leave,
    }
    return render(request, 'gate/leave_approve.html', context)


# ============= SALARY & PAYROLL =============

@login_required
def salary_structure(request):
    """View/Edit salary structure"""
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('employee_dashboard')
    
    employee_id = request.GET.get('employee_id')
    if not employee_id:
        return redirect('employee_list')
    
    employee = get_object_or_404(Employee, pk=employee_id)
    
    try:
        salary = employee.salary_structure
    except SalaryStructure.DoesNotExist:
        salary = None
    
    if request.method == 'POST':
        SalaryStructure.objects.update_or_create(
            employee=employee,
            defaults={
                'basic_salary': request.POST.get('basic_salary'),
                'hra': request.POST.get('hra', 0),
                'dearness_allowance': request.POST.get('dearness_allowance', 0),
                'conveyance': request.POST.get('conveyance', 0),
                'medical_allowance': request.POST.get('medical_allowance', 0),
                'other_allowances': request.POST.get('other_allowances', 0),
                'pf_contribution': request.POST.get('pf_contribution', 0),
                'esi_contribution': request.POST.get('esi_contribution', 0),
                'income_tax': request.POST.get('income_tax', 0),
                'other_deductions': request.POST.get('other_deductions', 0),
            }
        )
        return redirect('salary_structure', employee_id=employee_id)
    
    context = {
        'employee': employee,
        'salary': salary,
    }
    return render(request, 'gate/salary_structure.html', context)


@login_required
def payroll_processing(request):
    """Process payroll for a month"""
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('employee_dashboard')
    
    if request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('year')
        
        # Convert to proper types
        month_str = str(month).zfill(2)
        year_int = int(year)
        
        # Create or get payroll month
        payroll_month, created = PayrollMonth.objects.get_or_create(
            month=f"{year_int}-{month_str}",
            year=year_int,
            defaults={'status': 'DRAFT'}
        )
        
        # Process payroll for all employees
        employees = Employee.objects.filter(status='A')
        
        for employee in employees:
            try:
                salary_structure = employee.salary_structure
            except SalaryStructure.DoesNotExist:
                continue
            
            # Get attendance data
            month_start = datetime(int(year), int(month), 1).date()
            if int(month) == 12:
                month_end = datetime(int(year) + 1, 1, 1).date() - timedelta(days=1)
            else:
                month_end = datetime(int(year), int(month) + 1, 1).date() - timedelta(days=1)
            
            attendance_records = Attendance.objects.filter(
                employee=employee,
                date__range=[month_start, month_end]
            )
            
            present_days = attendance_records.filter(status='P').count()
            absent_days = attendance_records.filter(status='A').count()
            leave_days = attendance_records.filter(status__in=['L', 'ML', 'PL']).count()
            
            # Calculate salary
            working_days = 22  # Default working days
            
            payroll_record, created = PayrollRecord.objects.update_or_create(
                employee=employee,
                payroll_month=payroll_month,
                defaults={
                    'working_days': working_days,
                    'present_days': present_days,
                    'absent_days': absent_days,
                    'leave_days': leave_days,
                    'basic_salary': salary_structure.basic_salary,
                    'hra': salary_structure.hra,
                    'dearness_allowance': salary_structure.dearness_allowance,
                    'conveyance': salary_structure.conveyance,
                    'medical_allowance': salary_structure.medical_allowance,
                    'other_allowances': salary_structure.other_allowances,
                    'pf_contribution': salary_structure.pf_contribution,
                    'esi_contribution': salary_structure.esi_contribution,
                    'income_tax': salary_structure.income_tax,
                    'other_deductions': salary_structure.other_deductions,
                }
            )
            
            payroll_record.calculate_salary()
            payroll_record.save()
            
            # Create salary slip
            slip_number = f"SLIP-{payroll_month.month}-{employee.employee_id}"
            SalarySlip.objects.get_or_create(
                payroll_record=payroll_record,
                defaults={'slip_number': slip_number}
            )
        
        payroll_month.status = 'PROCESSED'
        payroll_month.processing_date = datetime.now()
        payroll_month.processed_by = request.user
        payroll_month.save()
        
        return redirect('payroll_records')
    
    context = {
        'months': range(1, 13),
        'current_year': datetime.now().year,
    }
    return render(request, 'gate/payroll_processing.html', context)


@login_required
def payroll_records(request):
    """View payroll records"""
    if not (request.user.is_staff or request.user.is_superuser):
        try:
            employee = Employee.objects.get(user=request.user)
            payroll_records = employee.payroll_records.all().order_by('-payroll_month')
        except Employee.DoesNotExist:
            return redirect('login')
    else:
        payroll_month = request.GET.get('payroll_month')
        payroll_records = PayrollRecord.objects.select_related('payroll_month').all()
        
        if payroll_month:
            payroll_records = payroll_records.filter(payroll_month_id=payroll_month)
        
        payroll_records = payroll_records.order_by('-payroll_month')
    
    payroll_months = PayrollMonth.objects.all().order_by('-year', '-month')
    
    context = {
        'payroll_records': payroll_records,
        'payroll_months': payroll_months,
    }
    return render(request, 'gate/payroll_records.html', context)


@login_required
def salary_slip_view(request, slip_id):
    """View salary slip"""
    salary_slip = get_object_or_404(SalarySlip, pk=slip_id)
    payroll_record = salary_slip.payroll_record
    employee = payroll_record.employee
    
    # Check if user has permission to view
    try:
        user_employee = Employee.objects.get(user=request.user)
        if user_employee.id != employee.id and not request.user.is_staff:
            return redirect('leave_list')
    except Employee.DoesNotExist:
        if not request.user.is_staff:
            return redirect('login')
    
    context = {
        'salary_slip': salary_slip,
        'payroll_record': payroll_record,
        'employee': employee,
    }
    return render(request, 'gate/salary_slip.html', context)


# ============= UTILITY FUNCTIONS =============

@login_required
def attendance_calendar(request, year=None, month=None):
    """Display attendance calendar"""
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        return redirect('employee_dashboard')
    
    today = datetime.now()
    if not year:
        year = today.year
    if not month:
        month = today.month
    
    # Get attendance for the month
    start_date = datetime(year, month, 1).date()
    if month == 12:
        end_date = datetime(year + 1, 1, 1).date() - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1).date() - timedelta(days=1)
    
    attendance_records = Attendance.objects.filter(
        employee=employee,
        date__range=[start_date, end_date]
    ).values('date', 'status')
    
    attendance_dict = {rec['date']: rec['status'] for rec in attendance_records}
    
    # Build calendar
    cal = monthcalendar(year, month)
    calendar_data = []
    
    for week in cal:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append(None)
            else:
                date_obj = datetime(year, month, day).date()
                status = attendance_dict.get(date_obj, None)
                week_data.append({
                    'day': day,
                    'status': status,
                    'date': date_obj,
                })
        calendar_data.append(week_data)
    
    context = {
        'employee': employee,
        'year': year,
        'month': month,
        'month_name': month_name[month],
        'calendar': calendar_data,
        'status_choices': Attendance._meta.get_field('status').choices,
    }
    return render(request, 'gate/attendance_calendar.html', context)
