from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model  # Import the get_user_model function

from attendance_system import settings
from .models import Admin, Student, Teacher
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
        # Construct the image filename
        image_filename = f"{student_id}.jpg"
        image_path = os.path.join(settings.MEDIA_ROOT, "Student_Images", image_filename)
        
        # Delete the image file if it exists
        try:
            os.remove(image_path)
        except FileNotFoundError:
            pass  # Image file not found
        
        # Delete the student from the database
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

# TEACHER HOME
def teacher_home(request):
    # Handle admin dashboard logic here
    return render(request, 'teacher_home.html')

# TEACHER LOGIN -----------------

# ADMIN HOME ----------------------

# @login_required  # Add this decorator to restrict access to authenticated users only
def admin_home(request):
    print("This is admin home")

    username = request.user.username  # Get the username of the logged-in user
    print(username)
    # Pass the username to the template
    return render(request, 'admin_home.html', {'username': username})


def login(request):
    if request.method == 'POST':
        # If the request method is POST, it means the form has been submitted
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print("Received username:", username)
        # print("Received password:", password)

        # Retrieve the Admin object based on the provided username
        try:
            admin = Admin.objects.get(username=username)
            # print("Admin found in the database:", admin)
            # print(admin.username, admin.password)
        except Admin.DoesNotExist:
            print("No admin found")
            admin = None

        admin = Admin.objects.filter(username=username).first()  # Retrieve the Admin object
        if admin and admin.username == username and admin.password == password:
            # Authentication successful, log in the user
            user = authenticate(request, username= admin.username, password=admin.password)
            print(user)
            if user is not None:
                auth_login(request, user)
            return redirect('admin_home')  # Redirect to admin_home page
        else:
            # Invalid username or password, render login page with alert
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html', {'username': username})

    else:
        return render(request, 'login.html')

