# Quick Reference Guide - Gate Garments HR System

## 🚀 Getting Started (5 Minutes)

### 1. Activate Virtual Environment
```bash
cd c:\Users\Victus\Desktop\sakthi
.\env\Scripts\Activate.ps1
```

### 2. Navigate to Project
```bash
cd sakthi\garments
```

### 3. Start Development Server
```bash
python manage.py runserver
```

### 4. Open in Browser
```
http://localhost:8000
```

### 5. Login with Demo Credentials
```
Username: admin
Password: admin
```

---

## 🔑 Demo Login Credentials

| User Type | Username | Password |
|-----------|----------|----------|
| Administrator | admin | admin |
| Employee 1 | emp001 | emp001 |
| Employee 2 | emp002 | emp002 |

---

## 📍 Important URLs

### System URLs
```
Home:               http://localhost:8000
Login:              http://localhost:8000/login
Admin Panel:        http://localhost:8000/admin
Employee Dashboard: http://localhost:8000/employee-dashboard
Admin Dashboard:    http://localhost:8000/admin-dashboard
```

### Main Features
```
Employees:          http://localhost:8000/employees
Attendance:         http://localhost:8000/attendance
Leaves:             http://localhost:8000/leaves
Payroll:            http://localhost:8000/payroll/records
Salary Slips:       http://localhost:8000/payroll/salary-slip/1
```

---

## ⌨️ Common Commands

### Server Management
```bash
# Start development server
python manage.py runserver

# Start on different port
python manage.py runserver 8001

# Stop server
Ctrl + C
```

### Database
```bash
# Apply migrations
python manage.py migrate

# Create new migration
python manage.py makemigrations

# Check system
python manage.py check

# Shell access
python manage.py shell
```

### Admin
```bash
# Create superuser
python manage.py createsuperuser

# Setup demo data
python setup_demo_data.py
```

---

## 📊 System Features Quick Access

### Employee Dashboard (emp001)
1. View personal attendance
2. Request leave
3. Check salary slips
4. View pending leaves

### Admin Dashboard (admin)
1. View all employees
2. Mark attendance
3. Process payroll
4. Approve leaves

---

## 🎯 Common Tasks

### Mark Attendance (Admin Only)
1. Go to: /attendance
2. Select employee from dropdown
3. Choose status (Present/Absent/Leave/etc)
4. Enter check-in/out times (optional)
5. Click "Mark Attendance"

### Request Leave (Employee)
1. Go to: /leaves/request
2. Select leave type
3. Enter start and end date
4. Write reason
5. Click "Submit Request"

### Process Payroll (Admin Only)
1. Go to: /payroll/process
2. Select month and year
3. Click "Process Payroll"
4. System auto-calculates for all employees
5. Salary slips generated

### View Salary Slip (Employee)
1. Go to: /payroll/records
2. Find your salary slip
3. Click "View Slip"
4. Print or save as needed

---

## 📁 Key Files

```
Models:           gate/models.py
Views:            gate/views.py
Admin:            gate/admin.py
URLs:             gate/urls.py
Templates:        templates/gate/

Base Template:    templates/gate/base.html
Setup Script:     setup_demo_data.py
Documentation:    README.md, PROJECT_PLAN.md
```

---

## 🐛 Troubleshooting

### Issue: Port 8000 in use
```bash
# Use different port
python manage.py runserver 8001
```

### Issue: Database not found
```bash
# Run migrations
python manage.py migrate
```

### Issue: Can't login
```bash
# Recreate demo data
python setup_demo_data.py
```

### Issue: Static files not loading
```bash
# For development, should work automatically
# For production, run:
python manage.py collectstatic
```

---

## 🔧 Customization

### Add New Employee Status
Edit `gate/models.py`:
```python
STATUS_CHOICES = [
    # ... existing choices ...
    ('X', 'New Status'),
]
```

### Change Salary Components
Edit `gate/models.py` - `SalaryStructure` model:
```python
new_component = models.DecimalField(max_digits=10, decimal_places=2, default=0)
```

### Add New Leave Type
Edit `gate/models.py` - `Leave` model:
```python
LEAVE_TYPE_CHOICES = [
    # ... existing choices ...
    ('NL', 'New Leave Type'),
]
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| README.md | Setup and usage guide |
| PROJECT_PLAN.md | Technical documentation |
| IMPLEMENTATION_SUMMARY.md | Implementation details |
| QUICK_REFERENCE.md | This file |

---

## 🎓 Code Structure

### Models (gate/models.py)
- Department, Employee, SalaryStructure
- Attendance, Leave, PayrollMonth
- PayrollRecord, SalarySlip, Deduction
- HolidayCalendar

### Views (gate/views.py)
- Dashboard views
- Employee management views
- Attendance views
- Leave management views
- Payroll processing views

### Admin (gate/admin.py)
- Customized admin interface
- 10 admin classes
- Inline editing
- Advanced filtering

### Templates (templates/gate/)
- base.html - Master template
- login.html - Login page
- dashboard*.html - Dashboards
- employee*.html - Employee management
- attendance*.html - Attendance
- leave*.html - Leave management
- payroll*.html - Payroll
- salary_slip.html - Salary slip

---

## 🔒 Security Tips

✅ Change admin password after first login  
✅ Use strong passwords for employees  
✅ Don't share login credentials  
✅ Keep Django updated  
✅ Run system checks regularly  
✅ Backup database frequently  

---

## 📞 Help & Support

### For Documentation
- See README.md
- See PROJECT_PLAN.md
- Check code comments

### For Django Help
- https://docs.djangoproject.com
- https://www.djangoproject.com

### For Bootstrap Help
- https://getbootstrap.com/docs

---

## 💡 Tips & Tricks

### Fast Attendance Marking
1. Use the filter to find employees
2. Mark multiple at once
3. Use keyboard shortcuts (Tab key)

### Efficient Payroll Processing
1. Set all salary structures first
2. Complete attendance for the month
3. Approve all pending leaves
4. Then process payroll

### Report Generation
1. Use date filters for specific periods
2. Export to PDF for printing
3. Filter by department for analysis

---

## 🎯 Admin Checklist

- [ ] Create all employee salary structures
- [ ] Mark daily attendance
- [ ] Review pending leave requests
- [ ] Process monthly payroll
- [ ] Generate salary slips
- [ ] Backup database regularly
- [ ] Update employee information
- [ ] Manage departments

---

## ⏰ Monthly Workflow

### Week 1
- Complete attendance for last month
- Approve all pending leaves

### Week 2
- Configure salary for new employees
- Process last month's payroll
- Generate salary slips

### Week 3
- Start marking attendance for new month
- Handle employee requests

### Week 4
- Prepare for next month payroll
- Run reports
- Backup data

---

## 📊 Key Metrics to Monitor

- Employee attendance rate
- Leave utilization
- Payroll processing time
- System uptime
- Database size
- Active users

---

## 🚀 Performance Tips

1. **Mark Attendance**: Use the quick entry form
2. **View Reports**: Use filters to narrow results
3. **Process Payroll**: Do once monthly
4. **Database**: Back up weekly
5. **Cache**: Clear after system updates

---

## 🎨 UI Navigation Tips

### Sidebar Menu
- **Dashboard** - Quick overview
- **Employees** - Manage staff
- **Attendance** - Daily records
- **Leaves** - Leave management
- **Payroll** - Salary processing

### Quick Actions
- Top right: User profile dropdown
- Cards: Click for more details
- Tables: Sort by clicking headers
- Forms: Validation in real-time

---

## 📱 Mobile Access

The system works on mobile browsers:
- http://localhost:8000 (use IP address for mobile)
- Responsive design auto-adjusts
- Touch-friendly buttons
- Mobile-optimized forms

---

## 🔄 Backup & Restore

### Backup Database
```bash
# Copy the db.sqlite3 file
Copy-Item db.sqlite3 db.sqlite3.backup
```

### Restore Database
```bash
# Replace with backup
Copy-Item db.sqlite3.backup db.sqlite3
```

---

## 📝 Notes

- System uses SQLite3 (suitable for small/medium organizations)
- For larger scale, consider PostgreSQL
- All times are in server timezone
- Attendance records are immutable once created
- Payroll can be recalculated by reprocessing

---

**Version**: 1.0.0  
**Last Updated**: January 12, 2026  
**Status**: ✅ Production Ready

For detailed documentation, see README.md and PROJECT_PLAN.md
