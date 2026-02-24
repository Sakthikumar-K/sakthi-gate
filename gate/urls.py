from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('employee-dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Employee Management
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_add, name='employee_add'),
    path('employees/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    path('employees/<int:employee_id>/edit/', views.employee_edit, name='employee_edit'),
    path('employees/<int:employee_id>/delete/', views.employee_delete, name='employee_delete'),
    
    # Attendance
    path('attendance/', views.attendance_view, name='attendance_view'),
    path('attendance/report/', views.attendance_report, name='attendance_report'),
    path('attendance/calendar/<int:year>/<int:month>/', views.attendance_calendar, name='attendance_calendar'),
    path('attendance/calendar/', views.attendance_calendar, name='attendance_calendar_current'),
    
    # Leave Management
    path('leaves/', views.leave_list, name='leave_list'),
    path('leaves/request/', views.leave_request, name='leave_request'),
    path('leaves/<int:leave_id>/approve/', views.leave_approve, name='leave_approve'),
    
    # Salary & Payroll
    path('salary-structure/', views.salary_structure, name='salary_structure'),
    path('payroll/process/', views.payroll_processing, name='payroll_processing'),
    path('payroll/records/', views.payroll_records, name='payroll_records'),
    path('payroll/salary-slip/<int:slip_id>/', views.salary_slip_view, name='salary_slip_view'),
]
