![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)
![DRF](https://img.shields.io/badge/DRF-3.16-orange)

# 🏢 HR Management System

A **comprehensive HR Management System** built with **Django REST Framework (DRF)**.  
Designed to streamline **employee management, attendance tracking, leave management, overtime, and payroll processing**, with **role-based access control**, **audit logs**, and **automated workflows**.  
This system is scalable, secure, and ideal for organizations looking to reduce manual HR processes.

---

## ✨ Core Modules & Features

| Module               | Icon | Features                                                                                       | Status         |
|---------------------|------|-------------------------------------------------------------------------------------------------|----------------|
| Employee Management  | 👥   | Complete **CRUD operations** for employees, departments, and job titles. Manage profiles, roles, and reporting hierarchy. | ✅ Completed   |
| Attendance Tracking  | ⏰   | Track **punch-in/out**, detect **late arrivals** or **early exits**, and maintain **automated daily attendance records**. | ✅ Completed   |
| Leave Management     | 📋   | Employees can **request leaves**, and managers/HR can **approve or reject**. System automatically updates leave status and balances. | ✅ Completed   |
| Overtime Management  | 💰   | Submit and review **overtime requests**. Enables tracking of extra working hours for payroll processing. | ✅ Completed   |
| Payroll Calculation  | 📊   | Automatically compute **salaries based on attendance, leave, and overtime**. Ensures accurate and timely payroll generation. | 🚧 In Progress |
| Audit Logs           | 📝   | Maintain a detailed **history of changes** in attendance and employee records. Supports accountability and compliance. | ✅ Completed   |

---

## 🛡️ Security & Access Control

| Feature                | Icon  | Description                                                                                     |
|-----------------------|-------|-------------------------------------------------------------------------------------------------|
| Role-based Permissions | 🔐    | Restrict access based on roles such as **HR, Manager, Employee** to ensure sensitive data is secure. |
| JWT Authentication     | 🛡️    | Provides **secure token-based authentication**, with optional cookie handling for front-end apps. |
| Custom Permissions     | 🎛️    | Fine-grained permissions for performing specific actions like approving leaves or editing attendance. |

---

## ⚙️ Automation & Smart Features

| Feature                  | Icon | Description                                                                                   |
|--------------------------|------|-----------------------------------------------------------------------------------------------|
| Daily Attendance Creation | 📅   | **Automatically creates daily attendance records** for all employees using Celery tasks.     |
| Leave Balance Management  | 🔄   | **Carry-forward system** automatically updates unused leave balances each month.             |
| Auto Check-out            | ⏱️   | Automatically checks out employees who forget to punch out at the end of the day.           |
| Related Records Creation  | 🤖   | **Signals automatically create related records** such as EmployeeProfile, EmergencyContact, and History when a new employee is added. |

---

## 📂 Project Structure




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


