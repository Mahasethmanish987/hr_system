![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)
![DRF](https://img.shields.io/badge/DRF-3.16-orange)

# 🏢 HR Management System


A comprehensive HR Management System built with Django REST Framework (DRF).  
Streamlines employee management, attendance tracking, leave management, task management, overtime, and payroll processing, with role-based access control, audit logs, and automated workflows.  
This system is modular, scalable, and secure, ideal for organizations looking to reduce manual HR processes.

---

## ✨ Core Modules & Features

| Module               | Icon | Features                                                                                       | Status         |
|---------------------|------|-------------------------------------------------------------------------------------------------|----------------|
| Employee Management  | 👥   | Complete CRUD operations for employees, departments, and job titles. Manage profiles, roles, and reporting hierarchy. | ✅ Completed   |
| Attendance Tracking  | ⏰   | Track punch-in/out, detect late arrivals/early exits, maintain automated daily attendance records, and handle half-days and leave checks. | ✅ Completed   |
| Leave Management     | 📋   | Employees can request leaves, and managers/HR can approve/reject. System automatically updates leave status, balances, and handles leave overlaps. | ✅ Completed   |
| Task Management      | 📝   | Create and manage tasks, sub-tasks, and onboarding/offboarding tasks with role-based assignments. | ✅ Completed   |
| Overtime Management  | 💰   | Submit and review overtime requests. Tracks extra working hours for payroll processing. | ✅ Completed   |
| Payroll Calculation  | 📊   | Compute salaries based on attendance, leave, overtime, allowances, deductions, and taxes. Supports automatic payroll generation. | ✅ Completed   |
| Audit Logs           | 🗂️   | Maintain history of changes in attendance, employee records, and task assignments for accountability and compliance. | ✅ Completed   |

---

## 🛡️ Security & Access Control

| Feature                | Icon  | Description                                                                                     |
|-----------------------|-------|-------------------------------------------------------------------------------------------------|
| Role-based Permissions | 🔐    | Restrict access based on roles such as HR, Manager, Employee to protect sensitive data. |
| JWT Authentication     | 🛡️    | Provides secure token-based authentication with optional cookie handling. |
| Custom Permissions     | 🎛️    | Fine-grained permissions for tasks, leaves, attendance, and payroll actions. |

---

## ⚙️ Automation & Smart Features

| Feature                     | Icon | Description                                                                                   |
|-----------------------------|------|-----------------------------------------------------------------------------------------------|
| Daily Attendance Creation    | 📅   | Automatically creates daily attendance records for all employees using services/tasks. |
| Leave Balance Management     | 🔄   | Carry-forward system automatically updates unused leave balances monthly. |
| Auto Check-out               | ⏱️   | Automatically checks out employees who forget to punch out. |
| Related Records Creation     | 🤖   | Signals automatically create related records such as EmployeeProfile, EmergencyContact, and History when a new employee is added. |
| Task Assignment Automation   | ⚡   | Assigns tasks and subtasks dynamically based on employee role and department. |
| Payroll Calculations         | 💵   | Computes allowances, deductions, overtime, and taxes automatically. |


## 📂 Project Structure




📂 Project Structure
```
hr_system/
├── attendance_module/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── services/
│   │   └── attendance_services.py
│   ├── filters.py
│   ├── permissions.py
│   ├── factories.py
│   ├── signals.py
│   └── tests/
│       └── test_attendance.py
│
├── leave_module/
│   ├── models.py
│   ├── services/
│   │   └── leave_services.py
│   ├── filters.py
│   ├── permissions.py
│   ├── factories.py
│   ├── signals.py
│   └── tests/
│       └── tests_leave.py
│
├── employee_module/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── services/
│   │   └── employee_services.py
│   ├── filters.py
│   ├── permissions.py
│   ├── factories.py
│   ├── signals.py
│   └── tests/
│       └── tests_employee.py
│
├── auth_module/
│   ├── models.py
│   ├── services/
│   │   ├── authentication_service.py
│   │   └── token_service.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── signals.py
│   └── tests/
│       └── tests_auth.py
│
├── payroll_module/
│   ├── models.py
│   ├── services/
│   │   ├── payroll_services.py
│   │   ├── deduction_calculator.py
│   │   ├── allowance_calculator.py
│   │   └── tax_calculator.py
│   ├── factories.py
│   ├── signals.py
│   └── tests/
│       └── test_payroll.py
│
├── task_module/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── filters.py
│   ├── permissions.py
│   └── factories.py
│
├── hr_system/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── celery.py
│
├── conftest.py        # Global pytest fixtures
├── manage.py
└── requirements.txt


```


