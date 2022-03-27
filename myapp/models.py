from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField(unique= True)
    password = models.CharField(max_length = 20)
    otp = models.IntegerField(default = 459)
    is_active = models.BooleanField(default=True)
    is_verfied = models.BooleanField(default=False)
    role = models.CharField(max_length = 10)
    created_at= models.DateTimeField(auto_now_add=True,blank=False)
    updated_at = models.DateTimeField(auto_now = True, blank=False)
    firs_time_login= models.BooleanField(default=False)

class Doctor(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    profile_pic=models.FileField(upload_to='doctor_finder/images/',blank=True,default='default.png')
    firstname = models.CharField(max_length=50,blank=True)
    lastname = models.CharField(max_length=50,blank=True)
    department = models.CharField(max_length=50,blank=True)
    aboutme= models.CharField(max_length=500,blank=True)
    gender= models.CharField(max_length=50,blank=True)
    contectno= models.CharField(max_length=10,blank=True)
    city= models.CharField(max_length=50,blank=True)
    country= models.CharField(max_length=50,blank=True)
    terms= models.BooleanField(default=False)

class Patient(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    profile_pic = models.FileField(upload_to='doctor_finder/images/', blank=True, default='default.png')
    firstname = models.CharField(max_length=50,blank=True)
    lastname = models.CharField(max_length=50,blank=True)
    contectno=  models.CharField(max_length = 10,blank=True)
    gender = models.CharField(max_length= 10,blank=True)
    terms = models.BooleanField(default=False)

class Case(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    disease = models.CharField(max_length=100)
    symtoms = models.CharField(max_length=100)
    status = models.CharField(max_length=100,default='active')

class Appointment(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    case_id = models.ForeignKey(Case, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_status = models.CharField(max_length=10,default='active')
