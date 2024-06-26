from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

from attendance_system import settings
from .models import Admin, Student
from .forms import AdminForm, StudentForm
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
import face_recognition
import os

import cv2
import numpy as np



# INDEX ------------

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# STUDENT HOME -------------
def student_home(request):
    # Handle admin dashboard logic here
    return render(request, 'student_home.html')

# MANAGE STUDENTS ----------
def manage_students(request):
    # Add your logic here to manage students
    return render(request, 'manage_students.html')

# MANAGE ADMIN
def manage_admin(request):
    # Add your logic here to manage students
    return render(request, 'manage_admin.html')


# ADD ADMIN ----------
def add_admin(request):
    if request.method == 'POST':
        form = AdminForm(request.POST, request.FILES)
        if form.is_valid():
            admin = form.save(commit=False)
            admin.save()

            # Get the uploaded image
            uploaded_image = request.FILES['image']

            # Define the directory path to save images
            image_directory = os.path.join(settings.MEDIA_ROOT, 'Admin_Images')

            # Create the directory if it doesn't exist
            if not os.path.exists(image_directory):
                os.makedirs(image_directory)

            # Save the image with student_id as filename
            image_path = os.path.join(image_directory, f"{admin.admin_id}.jpg")
            with open(image_path, 'wb+') as destination:
                for chunk in uploaded_image.chunks():
                    destination.write(chunk)

            # Redirect to the same page after successful submission
            return redirect('add_admin')
    else:
        form = AdminForm()  # Define the form for GET request

    return render(request, 'add_admin.html', {'form': form})



# ADD STUDENTS ----------
def add_students(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()

            # Get the uploaded image
            uploaded_image = request.FILES['image']

            # Define the directory path to save images
            image_directory = os.path.join(settings.MEDIA_ROOT, 'Student_Images')

            # Create the directory if it doesn't exist
            if not os.path.exists(image_directory):
                os.makedirs(image_directory)

            # Save the image with student_id as filename
            image_path = os.path.join(image_directory, f"{student.student_id}.jpg")
            with open(image_path, 'wb+') as destination:
                for chunk in uploaded_image.chunks():
                    destination.write(chunk)

            # Redirect to the same page after successful submission
            return redirect('add_students')
    else:
        form = StudentForm()  # Define the form for GET request

    return render(request, 'add_students.html', {'form': form})

# UPDATE STUDENTS ----------
def update_students(request):
    query = request.GET.get('query', '')
    students = Student.objects.filter(name__icontains=query) if query else Student.objects.none()
    context = {'students': students, 'query': query}
    return render(request, 'update_students.html', context)

# UPDATE ADMIN ----------
def update_admin(request):
    query = request.GET.get('query', '')
    admins = Admin.objects.filter(name__icontains=query) if query else Admin.objects.none()
    context = {'admins': admins, 'query': query}
    return render(request, 'update_admin.html', context)

# EDIT STUDENT ----------
def edit_student(request, student_id):
    student = Student.objects.get(pk=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('update_students')  # Redirect to update_students page
    else:
        form = StudentForm(instance=student)
    return render(request, 'edit_student.html', {'form': form, 'student': student})

# EDIT ADMIN ----------
def edit_admin(request, admin_id):
    admin = Admin.objects.get(pk=admin_id)
    if request.method == 'POST':
        form = AdminForm(request.POST, request.FILES, instance=admin)
        if form.is_valid():
            form.save()
            return redirect('update_admin')  # Redirect to update_admin page
    else:
        form = AdminForm(instance=admin)
    return render(request, 'edit_admin.html', {'form': form, 'admin': admin})

# DELETE STUDENT -----------

def delete_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('update_students')
    else:
        return HttpResponseBadRequest("Invalid request method")
    
# DELETE ADMIN -----------

def delete_admin(request, admin_id):
    admin = get_object_or_404(Admin, pk=admin_id)
    if request.method == 'POST':
        admin.delete()
        return redirect('update_admin')
    else:
        return HttpResponseBadRequest("Invalid request method")

# STUDENT LOGIN ------------------

def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('student_home')
        else:
            return render(request, 'student_login.html', {'error_message': 'Invalid username or password'})
    return render(request, 'student_login.html')

# TEACHER HOME
def teacher_home(request):
    # Handle admin dashboard logic here
    return render(request, 'teacher_home.html')

# TEACHER LOGIN -----------------

def teacher_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('teacher_home')
        else:
            return render(request, 'teacher_login.html', {'error_message': 'Invalid username or password'})
    return render(request, 'teacher_login.html')


# ADMIN HOME ----------------------

def admin_home(request):
    # Handle admin dashboard logic here
    return render(request, 'admin_home.html')

# ADMIN LOGIN ---------------------

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_home')
        else:
            return render(request, 'admin_login.html', {'error_message': 'Invalid username or password'})
    return render(request, 'admin_login.html')


# IMAGE TRAINING AND RECOGNITION ---------

