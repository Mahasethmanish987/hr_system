🏢 HR Management System

A comprehensive HR Management System built with Django REST Framework (DRF) that streamlines employee management, attendance tracking, leave management, and payroll processing. Designed for scalability and ease of use, with role-based access control and automated workflows.

✨ Features
📌 Core Modules
Module	Icon	Features	Status
Employee Management	👥	Full CRUD operations for employees, departments, and job titles	✅
Attendance Tracking	⏰	Punch-in/out, late arrival/early exit detection, automated daily attendance creation	✅
Leave Management	📋	Request, approve, or reject leaves with automated status updates	✅
Overtime Management	💰	Submit and review overtime requests	✅
Payroll Calculation	📊	Automatically compute salaries based on attendance and leave data	🚧
Audit Logs	📝	Track all changes to attendance and employee records	✅
🛡️ Security & Access Control
Feature	Icon	Description
Role-based permissions	🔐	HR, Manager, Employee access levels
JWT Authentication	🛡️	Secure token-based authentication with cookie handling
Custom Permissions	🎛️	Granular access control for different user roles
⚙️ Automation Features
Feature	Icon	Description
Daily Attendance Creation	📅	Automated daily attendance records via Celery tasks
Leave Balance Management	🔄	Automated leave balance carry-forward system
Auto Check-out	⏱️	Automatic check-out at end of day for forgetful employees
Related Records Creation	🤖	Signals for automatic creation of related records

## 📂 Project Structure
```
hr_system/
├── attendance_module/
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── tasks.py
│ ├── utils.py
│ ├── filters.py # Supports filtering attendance records
│ └── permissions.py
├── employee_module/
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── filters.py # Supports filtering employees
│ └── permissions.py
├── leave_module/
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ └── filters.py # Supports filtering leave requests
├── task_module/
│ ├── models.py
│ ├── serializers.py
│ └── views.py
├── hr_system/
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── manage.py
└── requirements.txt

```





