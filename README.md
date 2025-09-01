![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)
![DRF](https://img.shields.io/badge/DRF-3.16-orange)

🏢 HR Management System

A comprehensive HR Management System built with Django REST Framework (DRF).
Streamlines employee management, attendance tracking, leave management, and payroll processing with role-based access control and automated workflows.

✨ Core Modules & Features
Module	Icon	Features	Status
Employee Management	👥	CRUD for employees, departments, job titles	✅ Completed
Attendance Tracking	⏰	Punch-in/out, late detection, automated daily records	✅ Completed
Leave Management	📋	Request, approve, reject leaves, automated status	✅ Completed
Overtime Management	💰	Submit and review overtime requests	✅ Completed
Payroll Calculation	📊	Automatic salary computation based on attendance & leave	🚧 In Progress
Audit Logs	📝	Track all changes to employee & attendance records	✅ Completed
🛡️ Security & Access Control
Feature	Icon	Description
Role-based Permissions	🔐	HR, Manager, Employee access levels
JWT Authentication	🛡️	Secure token-based authentication with cookie handling
Custom Permissions	🎛️	Fine-grained access control for different roles
⚙️ Automation Features
Feature	Icon	Description
Daily Attendance Creation	📅	Automated daily attendance via Celery tasks
Leave Balance Management	🔄	Automated carry-forward system for leave balances
Auto Check-out	⏱️	Automatically checks out employees at the end of the day
Related Records Creation	🤖	Signals to create EmployeeProfile, EmergencyContact, History on new employee
📂 Project Structure
```
hr_system/
├── attendance_module/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── tasks.py
│   ├── utils.py
│   ├── filters.py       # Supports filtering attendance records
│   └── permissions.py
├── employee_module/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── filters.py       # Supports filtering employees
│   └── permissions.py
├── leave_module/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── filters.py       # Supports filtering leave requests
├── task_module/
│   ├── models.py
│   ├── serializers.py
│   └── views.py
├── hr_system/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt```
