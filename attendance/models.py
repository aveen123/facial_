from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password


class Student(models.Model):
    name = models.CharField(max_length=100, default='')
    dob = models.DateField(default='2000-01-01')
    username = models.CharField(max_length=100, default='')
    password = models.CharField(max_length=100, default='')
    confirm_password = models.CharField(max_length=100, default='')
    student_id = models.CharField(max_length=100, default='')
    program = models.CharField(max_length=100, default='')
    semester = models.CharField(max_length=100, default='')
    section = models.CharField(max_length=100, default='')
    college_email = models.EmailField(default='')
    personal_email = models.EmailField(default='')
    phone = models.CharField(max_length=20, default='')
    address = models.TextField(default='Unknown')
    emergency_contact_person = models.CharField(max_length=100, default='')
    emergency_contact_phone = models.CharField(max_length=20, default='')
    picture = models.ImageField(upload_to='student_pictures', default='default_picture.jpg')


class Admin(models.Model):
    name = models.CharField(max_length=100, default='')
    dob = models.DateField(default='2000-01-01')
    admin_id = models.CharField(max_length=100, default='')
    username = models.CharField(max_length=100, default='')
    password = models.CharField(max_length=100, default='')
    confirm_password = models.CharField(max_length=100, default='')
    college_email = models.EmailField(default='')
    personal_email = models.EmailField(default='')
    phone = models.CharField(max_length=20, default='')
    address = models.TextField(default='Unknown')
    picture = models.ImageField(upload_to='admin_pictures', default='default_picture.jpg')

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add other teacher attributes like department, designation, etc.

