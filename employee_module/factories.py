import factory 
from django.contrib.auth  import get_user_model 
from employee_module.models import Employee ,Department,JobTitle,EmployeeStatus,EmployeeType

User=get_user_model()
class UserFactory(factory.django.DjangoModelFactory): 

    class Meta: 
        model=User 
        skip_postgeneration_save = True
    username=factory.Faker("user_name")
    email=factory.Faker("email")
    password=factory.PostGenerationMethodCall('set_password','default_password')

class DepartmentFactory(factory.django.DjangoModelFactory): 
    class Meta: 
        model=Department 
    name=factory.Faker('company')

class JobTitleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = JobTitle

    job_title = factory.Faker("job")
    department = factory.SubFactory(DepartmentFactory)

class EmployeeTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeeType

    name = factory.Faker("word")

class EmployeeStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeeStatus

    name = factory.Faker("word")


class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee

    user = factory.SubFactory(UserFactory)
    role = Employee.HR

    email = factory.Faker("email")
    phone_number = factory.Faker("phone_number")
    dob = factory.Faker("date_of_birth", minimum_age=22, maximum_age=60)
    gender = factory.Iterator([Employee.MALE, Employee.FEMALE, Employee.OTHER])
    current_address = factory.Faker("address")
    permanent_address = factory.Faker("address")
    date_of_joining = factory.Faker("date_this_decade")

    department = factory.SubFactory(DepartmentFactory)
    job_title = factory.SubFactory(JobTitleFactory)
    employee_type = factory.SubFactory(EmployeeTypeFactory)
    employee_status = factory.SubFactory(EmployeeStatusFactory)

    current_salary = 100000
    marital_status='married'

