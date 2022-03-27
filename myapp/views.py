from django.shortcuts import render,HttpResponseRedirect,reverse
from .models import *
from django.core.mail import send_mail #django unblit function
from random import randint
from .utils import sendemail #user created
from django.http import JsonResponse
from django.core import serializers
# Create your views here.
def index(request):
    uid = User.objects.get(email=request.session['email'])
    if uid.role == 'doctor':
        did = Doctor.objects.get(user_id=uid)
        c_did = Doctor.objects.all().count()
        c_cid =Case.objects.all().count()
        c_pid = Patient.objects.all().count()

        doctorid = Doctor.objects.get(user_id=request.session['id'])
        allcase = Case.objects.filter(doctor_id=doctorid).select_related('patient_id', "doctor_id")
        allappointment = Appointment.objects.filter(doctor_id=doctorid).select_related('patient_id', 'doctor_id')
        context = {
            'uid': uid, 'did': did,'c_did':c_did,'c_cid':c_cid,'c_pid':c_pid,'allcase':allcase,'allappointment':allappointment,
        }
        return render(request, 'doctor/dashboard/doctor_index.html', {'context': context})
    elif uid.role == 'patients':
        pid = Patient.objects.get(user_id=uid)
        context = {
            'uid': uid, 'pid': pid
        }
        return render(request, 'doctor/dashboard/patients_index.html', {'context': context})

def r_page(request):
    return render(request, 'doctor/authentication/register.html')

def login_page(request):
    if 'email' in request.session:
        uid = User.objects.get(email=request.session['email'])
        if uid.role=='doctor':
            did = Doctor.objects.get(user_id=uid)

            context = {
                'uid': uid, 'did': did,
            }
            return render(request, 'doctor/dashboard/doctor_index.html', {'context':context})
        elif uid.role=='patients':
            pid = Patient.objects.get(user_id=uid)
            context = {
                'uid':uid, 'pid':pid
            }
            return render(request,'doctor/dashboard/patients_index.html',{'context':context})
    else:
        return render(request, 'doctor/authentication/login.html')

def registration(request):

        role=request.POST['role']
        firstname=request.POST['firstname']
        email=request.POST['email']
        password=request.POST['password']
        terms=request.POST['terms']

        if terms=="accept" and role=="doctor":

            uid = User.objects.create(email=email,password=password,role=role)
            did = Doctor.objects.create(user_id=uid,firstname=firstname)
            send_mail('conformation mail','welcome docter finder!!','www.pythonproject@gmail.com',[email])
            s_msg ='Successfully Register!!'
            return render(request,'doctor/authentication/login.html',{'s_msg':s_msg})

        elif terms=="accept" and role=="patients":
            uid = User.objects.create(email=email, password=password, role=role)
            pid = Patient.objects.create(user_id=uid,firstname=firstname)
            send_mail('conformation mail', 'welcome docter finder!!', 'www.pythonproject@gmail.com', [email])
            s_msg ='Successfully Register!!'
            return render(request, 'doctor/authentication/login.html', {'s_msg': s_msg})
        else:
            e_msg ='term condition require!!'
            return render(request,'doctor/authentication/register.html',{'e_msg':e_msg})


def login_evalute(request):
    try:
        role=request.POST['role']
        email=request.POST['email']
        password=request.POST['password']

        uid=User.objects.get(email=email,password=password,role=role)
        print('<<<<<<<<uid.role>>>>>>>>>', uid.role)

        if uid:
            if uid.role=='doctor':
                if uid.password==password:

                    did=Doctor.objects.get(user_id=uid)
                    request.session['email']=uid.email
                    request.session['firsname']=did.firstname
                    request.session['id']=uid.id

                    c_did = Doctor.objects.all().count()
                    c_cid = Case.objects.all().count()
                    c_pid = Patient.objects.all().count()

                    doctorid = Doctor.objects.get(user_id=request.session['id'])
                    allcase = Case.objects.filter(doctor_id=doctorid).select_related('patient_id', "doctor_id")
                    allappointment = Appointment.objects.filter(doctor_id=doctorid).select_related('patient_id',
                                                                                                   'doctor_id')
                    context = {
                        'uid': uid, 'did': did, 'c_did': c_did, 'c_cid': c_cid, 'c_pid': c_pid, 'allcase': allcase,'allappointment':allappointment,
                    }
                    return render(request, 'doctor/dashboard/doctor_index.html', {'context': context})

                else:
                    e_msg = "password not matched!!"
                    return render(request, 'doctor/authentication/login.html', {'e_msg': e_msg})
            else:
                if uid.password == password:

                    pid =Patient.objects.get(user_id=uid)
                    request.session['email'] = uid.email
                    request.session['firsname'] = pid.firstname
                    request.session['id'] = uid.id
                    context = {
                        'uid': uid, 'pid': pid,
                    }
                    return render(request, 'doctor/dashboard/patients_index.html', {'context': context})
        else:
            e_msg = "all term  require!!"
            return render(request, 'doctor/authentication/login.html', {'e_msg': e_msg})
    except:
        e_msg = "all term  require!!!!"
        return render(request, 'doctor/authentication/login.html', {'e_msg': e_msg})

def logout(request):
    if "email" in request.session:
        del request.session['firsname']
        del request.session['email']
        del request.session['id']
        return render(request,'doctor/authentication/login.html')
    else:
        return render(request, 'doctor/authentication/login.html')

def forgot_password(request):
    return render(request,'doctor/authentication/forgot_password.html')


def SEND_OTP(request):
    try:
        email = request.POST['email']

        uid=User.objects.get(email=email)
        if uid:
            otp=randint(1111,9999)
            uid.otp=otp
            uid.save()
            if uid.role=='doctor':
                did=Doctor.objects.get(user_id=uid)

                context={
                    'did':did,
                    'otp':otp
                }
                sendemail('forgot-Password', 'mail_template', email, {'context':context})
                return render(request,'doctor/authentication/reset_password.html',{'email':email})
            else:
                pid =Patient.objects.get(user_id=uid)

                context={
                    'pid':pid,
                    'otp':otp,
                }
                sendemail('forgot-Password', 'mail_template', email, {'context': context})
                return render(request, 'doctor/authentication/reset_password.html', {'email': email})
    except:
        e_msg = 'User Does Not Exist!!'
        return render(request,'doctor/authentication/forgot_password.html',{'e_msg':e_msg})

def reset_password(request):
    email=request.POST['email']
    otp=request.POST['OTP']
    newpassword=request.POST['newpassword']
    repassword=request.POST['repassword']

    uid=User.objects.get(email=email)
    if str(uid.otp)==otp and newpassword==repassword:
        uid.password=newpassword
        uid.save()
        s_msg="Password Successfully Changed!!"
        return render(request,'doctor/authentication/login.html',{'s_msg':s_msg})
    else:
        e_msg="invalid otp or password!!"
        return render(request, 'doctor/authentication/reset_password.html', {'email': email,'e_msg':e_msg})

def doctor_profile(request):
    uid = User.objects.get(email=request.session['email'])
    did = Doctor.objects.get(user_id=uid)
    context = {
        'uid': uid, 'did': did,
    }
    return render(request,'doctor/doctor/profile.html',{'context':context})

def update_doctorprofile(request):
    uid = User.objects.get(email=request.session['email'])
    did = Doctor.objects.get(user_id=uid)

    firstname=request.POST['firstname']
    lastname=request.POST['lastname']
    department =request.POST['department']
    city=request.POST['city']
    country=request.POST['country']
    contectno=request.POST['contectno']

    if "profilepic" in request.FILES:
        profilepic=request.FILES['profilepic']
        did.profile_pic=profilepic
    if "gender" in request.POST:
        gender = request.POST['gender']
        did.gender = gender

    did.firstname=firstname
    did.lastname=lastname
    did.department = department
    did.city=city
    did.country=country
    did.contectno=contectno


    did.save()

    context = {
        'uid': uid, 'did': did,
    }
    return render(request, 'doctor/doctor/profile.html', {'context': context})

def all_doctors(request):
    uid = User.objects.get(email=request.session['email'])
    did = Doctor.objects.get(user_id=uid)
    data =Doctor.objects.all()
    context = {
        'uid': uid, 'did': did,'data':data,
    }
    return render(request,'doctor/doctor/doctors.html',{'context':context})

def specific_doctors(request,pk):
    # all doctor in one specific doctor view profile
    did_id = Doctor.objects.get(id=pk)

    uid = User.objects.get(email=request.session['email'])
    did = Doctor.objects.get(user_id=uid)

    context = {
        'uid': uid, 'did': did,'did_id':did_id,
    }
    return render(request, 'doctor/doctor/specific_doctor.html', {'context': context})

def view_doctors(request):
    #patients side
    uid = User.objects.get(email=request.session['email'])
    pid = Patient.objects.get(user_id=uid)

    data = Doctor.objects.all()
    context = {
        'uid': uid, 'pid': pid,'data':data
    }
    return render(request, 'doctor/patients/view-doctors.html', {'context': context})

def patients_profile(request):
    uid = User.objects.get(email=request.session['email'])
    pid = Patient.objects.get(user_id=uid)
    context = {
        'uid': uid, 'pid': pid,
    }
    return render(request,'doctor/patients/patients-profile.html',{'context':context})

def update_patientsprofile(request):
    uid = User.objects.get(email=request.session['email'])
    pid = Patient.objects.get(user_id=uid)

    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    contectno =request.POST['contectno']

    if "profilepic" in request.FILES:
        profilepic = request.FILES['profilepic']
        pid.profile_pic = profilepic

    if 'gender' in request.POST:
        gender = request.POST['gender']
        pid.gender=gender

    pid.firstname = firstname
    pid.lastname = lastname
    pid.contectno = contectno

    pid.save()

    context = {
        'uid': uid, 'pid': pid,
    }
    return render(request, 'doctor/patients/patients-profile.html', {'context': context})

#cases
def PatientList(request):
    p_data = Patient.objects.all()
    res = serializers.serialize("json", p_data)
    return JsonResponse(res,safe=False)

def new_case(request):
    uid = User.objects.get(email=request.session['email'])
    did = Doctor.objects.get(user_id=uid)
    p_data = Patient.objects.all()
    context ={
        'uid':uid,'did':did,'p_data':p_data,
    }
    return render(request, 'doctor/doctor/new-case.html', {'context':context})

def getpatientsdetails(request):
    patient_id = request.GET['id']
    print('<<<<<<patient-id>>>>>>',patient_id)
    patient_details = Patient.objects.filter(id=patient_id)
    print('<<<<<<<<<<patient-details>>>>>>>>>>>>',patient_details)
    res = serializers.serialize('json', patient_details)
    print('<<<<<<<<<<<res>>>>>>>>>>>',res)
    return JsonResponse(res, safe=False)

def AddNewCaseToDatabase(request):
    patient_id = request.GET['patientid']
    print('patient-id------>', patient_id)
    doctor_id = request.session['id']
    print('doctor-id----->', doctor_id)
    patient = Patient.objects.get(id=patient_id)
    print('>>>>>>>>>>>patient<<<<<<<<<<<<<<',patient)
    doctor = Doctor.objects.get(user_id=doctor_id)
    print('<<<<<<<<<<doctor>>>>>>>>>>',doctor)
    disease = request.GET['diseases']
    symptoms = request.GET['symptoms']
    Case.objects.create(patient_id=patient, doctor_id=doctor, disease=disease, symtoms=symptoms)
    return HttpResponseRedirect(reverse('all-case'))

def all_case(request):
    print("<<--id-->> ", request.session['id'])
    uid = User.objects.get(email=request.session['email'])
    did = Doctor.objects.get(user_id=uid)

    doctorid = Doctor.objects.get(user_id=request.session['id'])
    allcase = Case.objects.filter(doctor_id=doctorid).select_related('patient_id', "doctor_id")
    print(allcase)

    context= {
        'uid':uid,'did':did,'allcase':allcase
    }

    for i in allcase:
        print("--> p - name ", i.patient_id.firstname)
        print("--> d - name ", i.doctor_id.firstname)

    return render(request, "doctor/doctor/all-case.html", {'context': context})

def delete_case(request,pk):
    cid = Case.objects.get(id=pk)
    cid.delete()

    uid = User.objects.get(email=request.session['email'])
    did = Doctor.objects.get(user_id=uid)
    doctorid = Doctor.objects.get(user_id=request.session['id'])

    allcase = Case.objects.filter(doctor_id=doctorid).select_related('patient_id', "doctor_id")
    context = {
        'uid': uid, 'did': did, 'allcase': allcase
    }
    return render(request, "doctor/doctor/all-case.html", {'context': context})



def appointment(request):
    uid = User.objects.get(email=request.session['email'])
    pid = Patient.objects.get(user_id=uid)
    d_data = Doctor.objects.all()
    cid = Case.objects.filter(patient_id=pid)

    context = {
        'uid': uid, 'pid': pid,'d_data':d_data,'cid':cid
    }
    return render(request, 'doctor/appointment/book-appointment.html', {'context': context})
def book_appointment(request):
    uid = User.objects.get(email=request.session['email'])
    pid = Patient.objects.get(user_id=uid)
    d_data = Doctor.objects.all()
    cid = Case.objects.filter(patient_id=pid)

    doctor_id = request.POST['doctorid']
    doctor = Doctor.objects.get(user_id=doctor_id)
    patient_id = request.session['id']
    patient = Patient.objects.get(user_id=patient_id)
    appointment_date = request.POST['appointment_date']
    case_id = request.POST['caseid']
    case = Case.objects.get(id=case_id)


    Appointment.objects.create(doctor_id=doctor, patient_id=patient,appointment_date=appointment_date,case_id=case)
    s_msg = 'Succesfully Submit Appoinment!!'
    context = {
        'uid': uid, 'pid': pid,'d_data':d_data,'cid':cid,'s_msg':s_msg
    }

    return render(request, 'doctor/appointment/book-appointment.html', {'context': context})

def view_appointment(request):
    #doctor side
    uid = User.objects.get(email=request.session['email'])
    did = Doctor.objects.get(user_id=uid)
    doctorid = Doctor.objects.get(user_id=request.session['id'])
    allappointment = Appointment.objects.filter(doctor_id=doctorid).select_related('patient_id','doctor_id')
    context={
        'uid':uid,'did':did,'allappointment':allappointment
    }
    return render(request,'doctor/appointment/view-appointment.html',{'context':context})

def delete_appointment(request,pk):
    #doctor side
    aid = Appointment.objects.get(id=pk)
    aid.delete()

    uid = User.objects.get(email=request.session['email'])
    did = Doctor.objects.get(user_id=uid)
    doctorid = Doctor.objects.get(user_id=request.session['id'])
    allappointment = Appointment.objects.filter(doctor_id=doctorid).select_related('patient_id', 'doctor_id')
    context = {
        'uid': uid, 'did': did, 'allappointment': allappointment
    }
    return render(request, 'doctor/appointment/view-appointment.html', {'context': context})