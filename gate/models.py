from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from datetime import date

class Department(models.Model):
    """Store department information"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Departments"
        ordering = ['name']


class Employee(models.Model):
    """Store employee information"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('A', 'Active'),
        ('I', 'Inactive'),
        ('S', 'Suspended'),
        ('R', 'Retired'),
    ]
    
    employee_id = models.CharField(max_length=20, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    # Employment Details
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    designation = models.CharField(max_length=100)
    date_of_joining = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    
    # Contact Information
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    
    # Bank Details
    bank_name = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=30, blank=True)
    ifsc_code = models.CharField(max_length=11, blank=True)
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['employee_id']
        verbose_name_plural = "Employees"


class SalaryStructure(models.Model):
    """Define salary components for an employee"""
    COMPONENT_TYPE_CHOICES = [
        ('EARNING', 'Earning'),
        ('DEDUCTION', 'Deduction'),
    ]
    
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='salary_structure')
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    hra = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    dearness_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    conveyance = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    medical_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    other_allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    # Deductions
    pf_contribution = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    esi_contribution = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    income_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Salary Structure - {self.employee.full_name}"
    
    @property
    def gross_salary(self):
        """Calculate gross salary"""
        earnings = (self.basic_salary + self.hra + self.dearness_allowance + 
                   self.conveyance + self.medical_allowance + self.other_allowances)
        return earnings
    
    @property
    def total_deductions(self):
        """Calculate total deductions"""
        return (self.pf_contribution + self.esi_contribution + 
                self.income_tax + self.other_deductions)
    
    class Meta:
        verbose_name_plural = "Salary Structures"


class Attendance(models.Model):
    """Track daily attendance of employees"""
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Leave'),
        ('H', 'Half Day'),
        ('WFH', 'Work From Home'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=3, choices=STATUS_CHOICES)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.employee.employee_id} - {self.date} ({self.status})"
    
    class Meta:
        unique_together = ('employee', 'date')
        ordering = ['-date']
        verbose_name_plural = "Attendance Records"
        indexes = [
            models.Index(fields=['employee', 'date']),
            models.Index(fields=['date']),
        ]


class Leave(models.Model):
    """Track employee leaves"""
    LEAVE_TYPE_CHOICES = [
        ('SL', 'Sick Leave'),
        ('CL', 'Casual Leave'),
        ('EL', 'Earned Leave'),
        ('UL', 'Unpaid Leave'),
        ('ML', 'Maternity Leave'),
        ('PL', 'Paternity Leave'),
    ]
    
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves')
    leave_type = models.CharField(max_length=2, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    approval_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.get_leave_type_display()}"
    
    @property
    def number_of_days(self):
        """Calculate number of leave days"""
        return (self.end_date - self.start_date).days + 1
    
    class Meta:
        verbose_name_plural = "Leaves"
        ordering = ['-start_date']


class PayrollMonth(models.Model):
    """Track payroll processing for each month"""
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PROCESSED', 'Processed'),
        ('APPROVED', 'Approved'),
        ('PAID', 'Paid'),
    ]
    
    month = models.CharField(max_length=7)  # Format: YYYY-MM
    year = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    processing_date = models.DateTimeField(null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    remarks = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payroll - {self.month}"
    
    class Meta:
        verbose_name_plural = "Payroll Months"
        unique_together = ('month', 'year')
        ordering = ['-year', '-month']


class PayrollRecord(models.Model):
    """Store individual payroll records"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payroll_records')
    payroll_month = models.ForeignKey(PayrollMonth, on_delete=models.CASCADE, related_name='payroll_records')
    
    # Attendance Summary
    working_days = models.IntegerField(default=0)
    present_days = models.IntegerField(default=0)
    absent_days = models.IntegerField(default=0)
    leave_days = models.IntegerField(default=0)
    
    # Salary Components (Earnings)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    dearness_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    conveyance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medical_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Calculated Earnings
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Deductions
    pf_contribution = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    esi_contribution = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    income_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Calculated Deductions
    total_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Net Salary
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Additional Info
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.payroll_month.month}"
    
    def calculate_salary(self):
        """Auto-calculate salary components"""
        # Calculate gross salary
        self.gross_salary = (self.basic_salary + self.hra + self.dearness_allowance + 
                            self.conveyance + self.medical_allowance + self.other_allowances)
        
        # Calculate total deductions
        self.total_deductions = (self.pf_contribution + self.esi_contribution + 
                                self.income_tax + self.other_deductions)
        
        # Calculate net salary
        self.net_salary = self.gross_salary - self.total_deductions
        
        return self.net_salary
    
    class Meta:
        verbose_name_plural = "Payroll Records"
        unique_together = ('employee', 'payroll_month')
        ordering = ['-payroll_month']
        indexes = [
            models.Index(fields=['employee', 'payroll_month']),
        ]


class SalarySlip(models.Model):
    """Generate salary slip documents"""
    payroll_record = models.OneToOneField(PayrollRecord, on_delete=models.CASCADE, related_name='salary_slip')
    slip_number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateField(auto_now_add=True)
    
    # For PDF storage/tracking
    pdf_generated = models.BooleanField(default=False)
    generated_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Salary Slip - {self.slip_number}"
    
    class Meta:
        verbose_name_plural = "Salary Slips"
        ordering = ['-issue_date']


class Deduction(models.Model):
    """Additional one-time deductions (loans, etc.)"""
    DEDUCTION_TYPE_CHOICES = [
        ('LOAN', 'Loan'),
        ('ADVANCE', 'Advance'),
        ('FINE', 'Fine'),
        ('ADJUSTMENT', 'Adjustment'),
        ('OTHER', 'Other'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='deductions')
    deduction_type = models.CharField(max_length=20, choices=DEDUCTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    
    # Date Range
    from_date = models.DateField()
    to_date = models.DateField()
    
    # Installment Details (for loans)
    number_of_installments = models.IntegerField(null=True, blank=True)
    monthly_installment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    installments_paid = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.get_deduction_type_display()}"
    
    class Meta:
        verbose_name_plural = "Deductions"
        ordering = ['-created_at']


class HolidayCalendar(models.Model):
    """Store company holidays"""
    date = models.DateField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.date} - {self.name}"
    
    class Meta:
        verbose_name_plural = "Holiday Calendar"
        ordering = ['date']
