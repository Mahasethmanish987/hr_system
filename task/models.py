from django.db import models
from employee_module.models import Employee,TimeStamp,Department,JobTitle

class Task(TimeStamp):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    )

    PRIORITY_CHOICES = (
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_by = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, related_name="tasks_created"
    )
    priority = models.CharField(
        max_length=100, choices=PRIORITY_CHOICES, default="medium"
    )
    
    due_date = models.DateTimeField()
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True
    )
    assigned_to = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True
    )
    status = models.CharField(choices=STATUS_CHOICES,default='pending' ,null=True, blank=True)

    def __str__(self):
        return self.title




class SubTask(TimeStamp):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    )

    PRIORITY_CHOICES = (
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_by = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, related_name="subtasks_created"
    )
    priority = models.CharField(
        max_length=100, choices=PRIORITY_CHOICES, default="medium"
    )
    
    due_date = models.DateTimeField()
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True
    )
    assigned_to = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True
    )
    status = models.CharField(choices=STATUS_CHOICES,default='pending' , null=True, blank=True)
    parent_task=models.ForeignKey(Task,on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return self.title




class  OnboardingOffboardingTask(TimeStamp): 
    ONBOARDING=1
    OFFBOARDING=2 
    task_choice=(
        (ONBOARDING,"onboarding"),
        (OFFBOARDING,"offboarding"),
    )

    
    task_name = models.CharField(max_length=255)
    department=models.ForeignKey(Department,on_delete=models.SET_NULL,null=True,blank=True,related_name='department_task')
    job_title=models.ForeignKey(JobTitle,on_delete=models.SET_NULL,null=True,blank=True,related_name='task')
    applies_to_all=models.BooleanField(default=False)
    task_type=models.CharField(choices=task_choice,null=True,blank=True)
    made_by=models.ForeignKey(Employee,on_delete=models.SET_NULL,null=True,blank=True,related_name='emplyee_task')
    
    def __str__(self): 
        return self.task_name 
    

