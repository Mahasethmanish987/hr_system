# HR Management System

A comprehensive HR Management System built with Django REST Framework, designed to simplify employee management, attendance tracking, payroll calculation, and more.

---

## 🚀 Core Features

### Employee Management
- Create, update, and manage employee profiles
- Store emergency contacts and employee history

### Department & Job Management
- Organize employees into departments
- Assign managers and roles

### Role-Based Permissions
- Secure API endpoints for HR, Manager, and Employee roles

### Attendance System
- Check-in / Check-out
- Track late arrivals and early exits
- Automatic daily attendance creation

### Overtime Management
- Employees can request overtime
- HR/Managers can approve or reject requests

### Leave Management
- Apply for leaves
- HR/Managers approve/reject requests
- Attendance status auto-updates

### Working Summary
- Automatic calculation of worked hours, overtime, and total hours

### Audit Logs
- Track changes made to attendance and employee records

---

## 🛠️ Tech Stack
- **Backend:** Python, Django, Django REST Framework  
- **Database:** PostgreSQL  
- **Task Queue:** Celery + Redis  
- **Authentication:** JWT / Session-based  
- **Deployment:** Docker (optional)  

---

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


