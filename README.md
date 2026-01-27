# Gate Garments - Attendance, Payroll & Auto Salary System

## Project Overview

A comprehensive **Django-based HR Management System** for Gate Garments that automates attendance tracking, payroll processing, and salary management. The system features:

- ✅ **Employee Management** - Profile management with complete employee information
- ✅ **Attendance Tracking** - Daily check-in/check-out, calendar view, reports
- ✅ **Leave Management** - Leave requests with approval workflow
- ✅ **Salary Structure** - Flexible salary component configuration
- ✅ **Auto Payroll Processing** - Automatic salary calculations with deductions
- ✅ **Salary Slip Generation** - Digital salary slips with print/export
- ✅ **Role-Based Access** - Admin, Manager, and Employee dashboards
- ✅ **Professional UI** - Responsive design with Bootstrap 5

---

## Quick Start Guide

### Prerequisites
- Python 3.8+
- Django 5.2.10
- SQLite3 (included with Python)

### Installation & Setup

1. **Activate Virtual Environment**
   ```bash
   cd c:\Users\Victus\Desktop\sakthi
   .\env\Scripts\Activate.ps1
   ```

2. **Navigate to Project**
   ```bash
   cd sakthi\garments
   ```

3. **Run Migrations** (already done)
   ```bash
   python manage.py migrate
   ```

4. **Load Demo Data** (already done)
   ```bash
   python setup_demo_data.py
   ```

5. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

6. **Access the System**
   - Web Interface: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

---

## Login Credentials

| Role | Username | Password |
|------|----------|----------|
| **Admin** | admin | admin |
| **Employee 1** | emp001 | emp001 |
| **Employee 2** | emp002 | emp002 |

---

## System Features

### 1. Dashboard
- **Employee Dashboard**: View personal attendance, leaves, salary slips
- **Admin Dashboard**: Manage all employees, process payroll, view statistics

### 2. Employee Management
- Add/edit/delete employees
- Store personal, employment, contact, and bank details
- Manage employee status (Active/Inactive/Suspended/Retired)

### 3. Attendance System
- **Mark Attendance**: Daily attendance marking with check-in/out times
- **Attendance Calendar**: Visual monthly attendance calendar
- **Attendance Reports**: Filter by date range and employee
- **Status Types**: Present, Absent, Leave, Half Day, Work From Home

### 4. Leave Management
- **Leave Request**: Employees can request leave with reason
- **Leave Types**: Sick Leave, Casual Leave, Earned Leave, Maternity/Paternity Leave
- **Approval Workflow**: Admin review and approve/reject leaves
- **Leave Tracking**: Track pending, approved, and rejected leaves

### 5. Salary & Payroll

#### Salary Structure
- Basic salary
- Allowances: HRA, DA, Conveyance, Medical
- Deductions: PF, ESI, Income Tax, Other
- Real-time gross and net salary calculation

#### Payroll Processing
- Auto-calculate salary based on attendance
- Process payroll for entire month
- Generate salary slips
- Track payroll status (Draft → Processed → Approved → Paid)

#### Salary Slip
- Detailed salary breakdown
- Attendance summary
- Professional format for print/download
- Employee-specific viewing

---

## File Structure

```
sakthi/garments/
├── garments/                 # Project configuration
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
│
├── gate/                     # Main application
│   ├── models.py            # Database models (10 models)
│   ├── views.py             # Business logic (12+ views)
│   ├── admin.py             # Django admin customization
│   ├── urls.py              # App URL routing
│   ├── apps.py              # App configuration
│   └── migrations/          # Database migrations
│
├── templates/gate/          # HTML templates (13+ templates)
│   ├── base.html            # Base template with navigation
│   ├── login.html           # Login page
│   ├── employee_dashboard.html
│   ├── admin_dashboard.html
│   ├── employee_list.html
│   ├── attendance.html
│   ├── leave_list.html
│   ├── payroll_records.html
│   ├── salary_slip.html
│   └── ... (more templates)
│
├── static/                  # Static files (CSS, JS)
├── manage.py                # Django management script
├── setup_demo_data.py       # Demo data setup script
└── db.sqlite3               # Database file
```

---

## Database Models

### 1. **Department**
- Organization departments
- Description and metadata

### 2. **Employee**
- Core employee information
- Personal, employment, contact, and bank details
- Status tracking (Active/Inactive/Suspended/Retired)

### 3. **SalaryStructure**
- Employee salary components
- Earnings and deductions
- Auto-calculated gross and net salary

### 4. **Attendance**
- Daily attendance records
- Status, check-in, check-out times
- Remarks and tracking

### 5. **Leave**
- Leave request management
- Leave types, date range, approval status
- Approval tracking and dates

### 6. **PayrollMonth**
- Monthly payroll tracking
- Status workflow (Draft → Processed → Approved → Paid)
- Processing metadata

### 7. **PayrollRecord**
- Individual employee payroll calculations
- Attendance summary, salary components, deductions
- Final net salary calculation

### 8. **SalarySlip**
- Generated salary slip documents
- Slip tracking and PDF generation metadata

### 9. **Deduction**
- Additional deductions (loans, advances, fines)
- Installment tracking for loans

### 10. **HolidayCalendar**
- Company holidays and special days
- Used for attendance calculations

---

## Core Views & URLs

| URL | View | Purpose |
|-----|------|---------|
| `/` | dashboard | Role-based redirect |
| `/employee-dashboard/` | employee_dashboard | Employee overview |
| `/admin-dashboard/` | admin_dashboard | Admin statistics |
| `/employees/` | employee_list | Employee directory |
| `/attendance/` | attendance_view | Mark daily attendance |
| `/attendance/report/` | attendance_report | Attendance analytics |
| `/attendance/calendar/` | attendance_calendar | Visual calendar view |
| `/leaves/` | leave_list | Leave management |
| `/leaves/request/` | leave_request | New leave request |
| `/leaves/<id>/approve/` | leave_approve | Approve/reject leave |
| `/salary-structure/` | salary_structure | Configure salary |
| `/payroll/process/` | payroll_processing | Process monthly payroll |
| `/payroll/records/` | payroll_records | View payroll history |
| `/payroll/salary-slip/<id>/` | salary_slip_view | View salary slip |

---

## Key Features & Highlights

### 🎯 Unique Features

1. **Smart Payroll Calculation**
   - Automatic salary computation based on attendance
   - Flexible salary components
   - Real-time gross/net calculation

2. **Professional Salary Slips**
   - Detailed breakdown of earnings and deductions
   - Attendance summary
   - Print-ready format

3. **Role-Based Access Control**
   - Employees see only their data
   - Admins manage all employees
   - Permission-based filtering

4. **Attendance Analytics**
   - Calendar view with visual status
   - Monthly reports with filters
   - Attendance trends

5. **Leave Workflow**
   - Request → Review → Approval
   - Leave type support (sick, casual, earned, maternity, paternity)
   - Approval tracking

### 🎨 UI/UX Highlights

- **Modern Design**: Bootstrap 5 responsive framework
- **Color-Coded Status**: Easy visual identification
- **Interactive Dashboards**: Real-time statistics and metrics
- **Mobile Responsive**: Works on desktop and mobile
- **Intuitive Navigation**: Sidebar menu with role-based options
- **Professional Theme**: Corporate look and feel

---

## Admin Panel Features

Access Django Admin at: `/admin`

### Registered Models:
- ✅ Departments
- ✅ Employees (with inline editing)
- ✅ Salary Structures
- ✅ Attendance (with date hierarchy)
- ✅ Leaves (with approval workflow)
- ✅ Payroll Months
- ✅ Payroll Records (with calculated fields)
- ✅ Salary Slips
- ✅ Deductions
- ✅ Holiday Calendar

### Admin Features:
- Advanced filtering and search
- Bulk actions
- Inline editing
- Custom display formats
- Status badges with colors

---

## Technologies Used

- **Backend**: Django 5.2.10
- **Database**: SQLite3
- **Frontend**: Bootstrap 5, jQuery
- **Authentication**: Django's built-in auth system
- **ORM**: Django ORM
- **Forms**: Django forms

---

## Customization Guide

### Add New Employee Status
Edit `gate/models.py` in the `Employee` model:
```python
STATUS_CHOICES = [
    ('A', 'Active'),
    ('I', 'Inactive'),
    ('S', 'Suspended'),
    ('R', 'Retired'),
    ('L', 'On Leave'),  # Add new status
]
```

### Modify Salary Components
Edit `SalaryStructure` model in `gate/models.py`:
```python
special_bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
```

### Add New Leave Type
Edit `Leave` model:
```python
LEAVE_TYPE_CHOICES = [
    # ... existing choices ...
    ('BL', 'Bereavement Leave'),  # Add new
]
```

---

## Future Enhancements

1. **Email Notifications**
   - Leave approval/rejection notifications
   - Salary slip email delivery

2. **PDF Export**
   - Generate PDF salary slips
   - Export reports as PDF/Excel

3. **Biometric Integration**
   - Import attendance from biometric devices
   - Time-based attendance tracking

4. **Mobile App**
   - Native mobile application
   - Self-service leave requests

5. **Advanced Analytics**
   - Attendance trends
   - Payroll analytics
   - Department-wise reports

6. **Performance Tracking**
   - Employee performance ratings
   - Increment management

---

## Troubleshooting

### Issue: "No such table" error
**Solution**: Run migrations again
```bash
python manage.py migrate
```

### Issue: Static files not loading
**Solution**: Collect static files
```bash
python manage.py collectstatic
```

### Issue: Can't login
**Solution**: Run demo setup again
```bash
python setup_demo_data.py
```

### Issue: Port 8000 already in use
**Solution**: Use different port
```bash
python manage.py runserver 8001
```

---

## Security Considerations

- ✅ CSRF protection enabled
- ✅ SQL injection prevention (Django ORM)
- ✅ XSS protection enabled
- ✅ Password hashing
- ✅ Role-based access control
- ⚠️ Debug mode disabled in production
- ⚠️ Change SECRET_KEY in production

---

## Support & Documentation

- **Django Official Docs**: https://docs.djangoproject.com/
- **Bootstrap 5 Docs**: https://getbootstrap.com/
- **Project Issues**: Contact your development team

---

## License

All rights reserved © 2026 Gate Garments

---

**Version**: 1.0.0  
**Last Updated**: January 12, 2026  
**Status**: Production Ready ✅
#   s a k t h i - g a t e  
 