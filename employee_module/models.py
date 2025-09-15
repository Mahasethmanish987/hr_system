import datetime

from django.contrib.auth import get_user_model
from django.db import models


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True



class Department(TimeStamp):
    name = models.CharField(max_length=255, unique=True)
    department_code = models.CharField(max_length=255, blank=True)
    manager = models.OneToOneField(
        "Employee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_department",
    )

    def __str__(self): 
        return self.name 

    def save(self, *args, **kwargs):
        if not self.department_code:
            prefix = self.name[:3].upper()

            last_count = last_count = Department.objects.count() + 1
            self.department_code = f"{prefix}{last_count:03d}"
        super().save(*args, **kwargs)


class JobTitle(TimeStamp):
    job_title = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, null=False, blank=False
    )
    
    def __str__(self): 
        return self.job_title 


class EmployeeType(TimeStamp):
    name = models.CharField(unique=True, max_length=255)

    def __str__(self): 
        return self.name 


class EmployeeStatus(TimeStamp):
    name = models.CharField(unique=True, max_length=255)

    def __str__(self): 
        return self.name 


User = get_user_model()


class Employee(TimeStamp):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"

    choices = ((MALE, "male"), (FEMALE, "female"), (OTHER, "O"))
    marital_choices=(('married',"Married"),("unmarried","Unmarried"))
    HR = 1
    MANAGER = 2
    OTHER = 3
    role_choices = ((HR, "hr"), (MANAGER, "manager"), (OTHER, "other"))
    user = models.OneToOneField(User, on_delete=models.RESTRICT,related_name='employee')
    role = models.PositiveSmallIntegerField(choices=role_choices, default=3)

    employee_code = models.CharField(max_length=255, unique=True,blank=True)
    email = models.EmailField(unique=True, max_length=255)
    phone_number = models.CharField(max_length=20, unique=True)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=choices, null=True, blank=True)
    current_address = models.CharField(max_length=255)
    permanent_address = models.CharField(max_length=255)
    reporting_manager = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    date_of_joining = models.DateField(default=datetime.date.today)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees",
    )
    job_title = models.ForeignKey(JobTitle, on_delete=models.PROTECT)
    employee_type = models.ForeignKey(
        EmployeeType, on_delete=models.SET_NULL, null=True, blank=True
    )
    employee_status = models.ForeignKey(
        EmployeeStatus, on_delete=models.SET_NULL, null=True, blank=True
    )
    current_salary = models.DecimalField(max_digits=10, decimal_places=2)
    marital_status=models.CharField(choices=marital_choices,max_length=20,default='unmarried')

    def __str__(self): 
        return f"{self.user.username}--{self.job_title}"

    def save(self, *args, **kwargs):
        if not self.employee_code:
            
            dept_code = self.department.name[:3].upper() if self.department else "GEN"

           
            join_date = self.date_of_joining.strftime("%Y%m")

            
            existing_count = (
                Employee.objects.filter(
                    department=self.department,
                    date_of_joining__year=self.date_of_joining.year,
                    date_of_joining__month=self.date_of_joining.month,
                ).count()
                + 1
            )  
            self.employee_code = f"{dept_code}-{join_date}-{existing_count:03d}"

        super().save(*args, **kwargs)


class EmergencyContact(TimeStamp):
    FATHER = 1
    MOTHER = 2
    WIFE = 3
    CHOICES = (
        (FATHER, "father"),
        (MOTHER, "mother"),
        (WIFE, "wife"),
    )
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL,blank=True,null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    relationship = models.PositiveSmallIntegerField(
        choices=CHOICES, null=True, blank=True
    )
    contact_number = models.CharField(max_length=20,null=True,blank=True)


class EmployeeProfile(TimeStamp):
    employee = models.OneToOneField(Employee, on_delete=models.SET_NULL,blank=True,null=True)
    profile_photo = models.FileField(
        upload_to="employee/profile/profile_photo", blank=True, null=True
    )
    citizenship = models.FileField(
        upload_to="employee/profile/citizenship", blank=True, null=True
    )
    pan_card = models.FileField(
        upload_to="employee/profile/pancard/", null=True, blank=True
    )
    contact_agreement = models.FileField(
        upload_to="employee/profile/contactaggreement/", null=True, blank=True
    )


class EmployeeHistory(TimeStamp):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL,null=True,blank=True)
    previous_company = models.CharField(max_length=255, null=True, blank=True)
    previous_position = models.CharField(max_length=255, null=True, blank=True)
    previous_salary = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )


class EmployeeTask(TimeStamp):
    ONBOARDING = 1
    OFFBOARDING = 2
    task_choices = (
        (ONBOARDING, "onboarding"),
        (OFFBOARDING, "offboarding"),
    )
    employee_task_name = models.CharField(max_length=255)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True
    )
    job_title = models.ForeignKey(
        JobTitle, on_delete=models.SET_NULL, null=True, blank=True
    )
    applies_to = models.BooleanField(default=False)
    employee_task_type = models.CharField(choices=task_choices, null=True, blank=True)


class EmployeeTaskCompletion(TimeStamp):
    employee_task = models.ForeignKey(EmployeeTask, on_delete=models.SET_NULL,null=True,blank=True)
    performed_by_department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True
    )
    completed_task = models.BooleanField(default=False)

