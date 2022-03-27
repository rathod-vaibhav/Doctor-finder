"""docter_finder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('r-page/', views.r_page, name='r-page'),
    path('login-page/', views.login_page, name='login-page'),

    path('registration/', views.registration, name='registration'),
    path('login-evalute/', views.login_evalute, name='login-evalute'),
    path('logout/', views.logout, name='logout'),

    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('SEND-OTP', views.SEND_OTP, name='SEND-OTP'),
    path('reset-password/', views.reset_password, name='reset-password'),

    path('doctor-profile/', views.doctor_profile, name='doctor-profile'),
    path('update-doctorprofile/', views.update_doctorprofile, name='update-doctorprofile'),

    path('all-doctors/', views.all_doctors, name='all-doctors'),  # doctor view
    path('specific-doctors/<int:pk>', views.specific_doctors, name='specific-doctors'),

    path('view-doctors/', views.view_doctors, name='view-doctors'),  # patients view

    path('patients-profile/', views.patients_profile, name='patients-profile'),
    path('update-patientsprofile/', views.update_patientsprofile, name='update-patientsprofile'),

    path('new-case/', views.new_case, name='new-case'),
    path('get-patients-details/', views.getpatientsdetails, name='get-patients-details'),
    path('create-new-case/', views.AddNewCaseToDatabase, name="create-new-case"),
    path('all-case/', views.all_case, name='all-case'),
    path('delete-case/<int:pk>', views.delete_case, name='delete-case'),

    path('appointment/', views.appointment, name='appointment'),
    path('book-appointment/', views.book_appointment, name='book-appointment'),
    path('view-appointmnet/',views.view_appointment,name='view-appointment'),
    path('delete-appointment/<int:pk>',views.delete_appointment,name='delete-appointment'),

]
