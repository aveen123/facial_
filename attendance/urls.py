from django.urls import path
from . import views

urlpatterns = [
    
    # index -----------
    path('', views.index, name= 'index'),

    # Student ---------------
    path('student/', views.student_home, name='student_home'),
    path('student/manage_students/', views.manage_students, name='manage_students'),
    path('student/manage_students/add-students/', views.add_students, name='add_students'),
    path('student/manage_students/update_students/', views.update_students, name='update_students'),
    path('student/manage_students/update_students/edit_student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('student/manage_students/update_students/delete_student/<int:student_id>/', views.delete_student, name='delete_student'),


    # Teacher ---------------------
    path('teacher/', views.teacher_home, name='teacher_home'),

    # Admin -------------------------
    path('admin/home/', views.admin_home, name='admin_home'),
    path('manage_admin/', views.manage_admin, name='manage_admin'),
    path('manage_admin/add-admin/', views.add_admin, name='add_admin'),
    path('manage_admin/update_admin/', views.update_admin, name='update_admin'),
    path('manage_admin/update_admin/edit_admin/<int:admin_id>/', views.edit_admin, name='edit_admin'),
    path('manage_admin/update_admin/delete_admin/<int:admin_id>/', views.delete_admin, name='delete_admin'),
    


    path('login/', views.login, name='login'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),


    # path('train/', views.train_image, name='train_image'),
    # path('save_image/', views.save_image, name='save_image'),


]
