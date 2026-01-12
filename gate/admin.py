from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Department, Employee, SalaryStructure, Attendance, Leave, 
    PayrollMonth, PayrollRecord, SalarySlip, Deduction, HolidayCalendar
)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'full_name', 'email', 'department', 'designation', 'status', 'date_of_joining')
    list_filter = ('status', 'department', 'date_of_joining')
    search_fields = ('employee_id', 'first_name', 'last_name', 'email')
    fieldsets = (
        ('Personal Information', {
            'fields': ('employee_id', 'user', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'gender')
        }),
        ('Employment Details', {
            'fields': ('department', 'designation', 'date_of_joining', 'status')
        }),
        ('Contact Information', {
            'fields': ('address', 'city', 'state', 'postal_code')
        }),
        ('Bank Details', {
            'fields': ('bank_name', 'account_number', 'ifsc_code')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('employee_id',)


@admin.register(SalaryStructure)
class SalaryStructureAdmin(admin.ModelAdmin):
    list_display = ('employee', 'basic_salary', 'gross_salary_display', 'total_deductions_display')
    search_fields = ('employee__first_name', 'employee__last_name', 'employee__employee_id')
    fieldsets = (
        ('Employee', {
            'fields': ('employee',)
        }),
        ('Earnings', {
            'fields': ('basic_salary', 'hra', 'dearness_allowance', 'conveyance', 'medical_allowance', 'other_allowances')
        }),
        ('Deductions', {
            'fields': ('pf_contribution', 'esi_contribution', 'income_tax', 'other_deductions')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def gross_salary_display(self, obj):
        return f"₹{obj.gross_salary:,.2f}"
    gross_salary_display.short_description = 'Gross Salary'
    
    def total_deductions_display(self, obj):
        return f"₹{obj.total_deductions:,.2f}"
    total_deductions_display.short_description = 'Total Deductions'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status_badge', 'check_in_time', 'check_out_time')
    list_filter = ('status', 'date', 'employee__department')
    search_fields = ('employee__first_name', 'employee__last_name', 'employee__employee_id')
    date_hierarchy = 'date'
    fieldsets = (
        ('Attendance Details', {
            'fields': ('employee', 'date', 'status')
        }),
        ('Time Tracking', {
            'fields': ('check_in_time', 'check_out_time')
        }),
        ('Additional Info', {
            'fields': ('remarks',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def status_badge(self, obj):
        colors = {
            'P': '#28a745',  # Green
            'A': '#dc3545',  # Red
            'L': '#ffc107',  # Yellow
            'H': '#17a2b8',  # Blue
            'WFH': '#6f42c1',  # Purple
        }
        return format_html(
            '<span style="color: white; background-color: {}; padding: 3px 8px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, '#333'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'number_of_days', 'status_badge')
    list_filter = ('status', 'leave_type', 'start_date')
    search_fields = ('employee__first_name', 'employee__last_name', 'employee__employee_id')
    fieldsets = (
        ('Leave Details', {
            'fields': ('employee', 'leave_type', 'start_date', 'end_date', 'reason')
        }),
        ('Approval', {
            'fields': ('status', 'approved_by', 'approval_date')
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'number_of_days')
    
    def status_badge(self, obj):
        colors = {
            'P': '#ffc107',  # Yellow
            'A': '#28a745',  # Green
            'R': '#dc3545',  # Red
        }
        return format_html(
            '<span style="color: white; background-color: {}; padding: 3px 8px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, '#333'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(PayrollMonth)
class PayrollMonthAdmin(admin.ModelAdmin):
    list_display = ('month', 'year', 'status', 'processing_date', 'payment_date')
    list_filter = ('status', 'year', 'month')
    search_fields = ('month',)
    fieldsets = (
        ('Payroll Period', {
            'fields': ('month', 'year')
        }),
        ('Processing', {
            'fields': ('status', 'processing_date', 'payment_date', 'processed_by')
        }),
        ('Remarks', {
            'fields': ('remarks',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-year', '-month')


@admin.register(PayrollRecord)
class PayrollRecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'payroll_month', 'gross_salary_display', 'total_deductions_display', 'net_salary_display')
    list_filter = ('payroll_month', 'employee__department')
    search_fields = ('employee__first_name', 'employee__last_name', 'employee__employee_id')
    fieldsets = (
        ('Employee & Period', {
            'fields': ('employee', 'payroll_month')
        }),
        ('Attendance Summary', {
            'fields': ('working_days', 'present_days', 'absent_days', 'leave_days')
        }),
        ('Earnings', {
            'fields': ('basic_salary', 'hra', 'dearness_allowance', 'conveyance', 'medical_allowance', 'other_allowances', 'gross_salary')
        }),
        ('Deductions', {
            'fields': ('pf_contribution', 'esi_contribution', 'income_tax', 'other_deductions', 'total_deductions')
        }),
        ('Net Salary', {
            'fields': ('net_salary',)
        }),
    )
    readonly_fields = ('gross_salary', 'total_deductions', 'net_salary', 'created_at', 'updated_at')
    
    def gross_salary_display(self, obj):
        return f"₹{obj.gross_salary:,.2f}"
    gross_salary_display.short_description = 'Gross'
    
    def total_deductions_display(self, obj):
        return f"₹{obj.total_deductions:,.2f}"
    total_deductions_display.short_description = 'Deductions'
    
    def net_salary_display(self, obj):
        return format_html(
            '<strong style="color: green;">₹{:,.2f}</strong>',
            obj.net_salary
        )
    net_salary_display.short_description = 'Net Salary'


@admin.register(SalarySlip)
class SalarySlipAdmin(admin.ModelAdmin):
    list_display = ('slip_number', 'employee_name', 'month', 'net_salary_display', 'pdf_status', 'issue_date')
    list_filter = ('issue_date', 'payroll_record__payroll_month')
    search_fields = ('slip_number', 'payroll_record__employee__employee_id')
    readonly_fields = ('created_at', 'updated_at', 'slip_number', 'payroll_record')
    
    def employee_name(self, obj):
        return obj.payroll_record.employee.full_name
    employee_name.short_description = 'Employee'
    
    def month(self, obj):
        return obj.payroll_record.payroll_month.month
    month.short_description = 'Payroll Month'
    
    def net_salary_display(self, obj):
        return f"₹{obj.payroll_record.net_salary:,.2f}"
    net_salary_display.short_description = 'Net Salary'
    
    def pdf_status(self, obj):
        if obj.pdf_generated:
            return format_html('<span style="color: green;">✓ Generated</span>')
        return format_html('<span style="color: red;">✗ Pending</span>')
    pdf_status.short_description = 'PDF Status'


@admin.register(Deduction)
class DeductionAdmin(admin.ModelAdmin):
    list_display = ('employee', 'deduction_type', 'amount', 'from_date', 'to_date', 'is_active')
    list_filter = ('deduction_type', 'is_active', 'from_date')
    search_fields = ('employee__first_name', 'employee__last_name', 'employee__employee_id')
    fieldsets = (
        ('Employee', {
            'fields': ('employee',)
        }),
        ('Deduction Details', {
            'fields': ('deduction_type', 'amount', 'description')
        }),
        ('Date Range', {
            'fields': ('from_date', 'to_date')
        }),
        ('Installment Details', {
            'fields': ('number_of_installments', 'monthly_installment', 'installments_paid')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(HolidayCalendar)
class HolidayCalendarAdmin(admin.ModelAdmin):
    list_display = ('date', 'name', 'created_at')
    list_filter = ('date',)
    search_fields = ('name',)
    date_hierarchy = 'date'
    readonly_fields = ('created_at', 'updated_at')
