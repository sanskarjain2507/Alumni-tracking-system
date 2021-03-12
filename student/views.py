from django.shortcuts import render
from Admin.models import User_data,Admin
from django.contrib.auth import authenticate,login,logout
from college.models import College,Consensus,Notice
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from .models import Student
import json
import smtplib
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
from googlegeocoder import GoogleGeocoder
from  geopy.geocoders import Nominatim
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
import base64
import traceback
from cryptography.fernet import Fernet
from django.conf import settings
import logging
import requests
from collections import OrderedDict

def encrypt(txt):
    try:
        # convert integer etc to string first
        txt = str(txt)
        # get the key from settings
        cipher_suite = Fernet(settings.ENCRYPT_KEY) # key should be byte
        # #input should be byte, so convert the text to byte
        encrypted_text = cipher_suite.encrypt(txt.encode('ascii'))
        # encode to urlsafe base64 format
        encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("ascii")
        return encrypted_text
    except Exception as e:
        # log the error if any
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


def decrypt(txt):
    try:
        # base64 decode
        txt = base64.urlsafe_b64decode(txt)
        cipher_suite = Fernet(settings.ENCRYPT_KEY)
        decoded_text = cipher_suite.decrypt(txt).decode("ascii")
        return decoded_text
    except Exception as e:
        # log the error
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None

@login_required()
def student_homepage(request):
    role = request.GET.get("role")
    username = request.GET.get("username")
    if role == 'student':
        student = Student.objects.filter(emailAdd=username)
        param = {'role': role, 'username': username,'student':student[0]}
        return render(request, 'student/student_homepage.html', param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

def signup_here(request):
    clg=College.objects.order_by('collegeName').values('collegeName').distinct()
    clg=list(clg)
    colleges=[]
    for i in clg:
        for j in i.values():
            colleges.append(j)

    # print(colleges)
    depts = ['CSE', 'IT', 'CIVIL', 'MECH', 'ETC']
    sts=['Job','Buissness','Yet to be placed','Startup','Others']
    return render(request,'student/signup_page.html',{'sts':sts,'depts':depts,'role':'student','colleges':colleges})


@csrf_exempt
def student_login_success(request):
    username1 = request.POST.get('username1')
    password1 = request.POST.get('password1')
    print(encrypt(password1))
    isUser = User_data.objects.filter(emailAdd=username1).exists()
    if isUser != False:
        user = (User_data.objects.filter(emailAdd=username1))[0].role
        if user == 'college':
            users = College.objects.all()
            for u in users:
                if u.emailAdd == username1:

                    if decrypt(u.password) == password1:
                        user = authenticate(request, username=username1, password=password1)
                        print(user)
                        if user == None:
                            User.objects.create_user(username=username1, password=password1)
                            user = authenticate(request, username=username1, password=password1)
                            print(user)
                        if user is not None:
                            request.session['logged_user'] = username1
                            login(request, user)
                        role = 'college'
                        params = {'username': username1, 'role': role}
                        return render(request, 'college/college_homepage.html', params)
                    else:
                        print(password1)
                        return render(request, 'Admin/login_page.html', {'pass_error': 'Incorrect Password'})
        elif user == 'admin':
            users = Admin.objects.all()
            for u in users:
                if u.emailAdd == username1:
                    #ADMIN IS PASSWORD

                    if decrypt(u.password) == password1:
                        user = authenticate(request, username=username1, password=password1)
                        print(user)
                        if user == None:
                            User.objects.create_user(username=username1, password=password1)
                            user = authenticate(request, username=username1, password=password1)
                        print(user)
                        if user is not None:
                            login(request, user)
                        role = 'admin'
                        params = {'username': username1, 'role': role}
                        return render(request, 'Admin/admin_homepage.html', params)
                    else:
                        print(password1)
                        return render(request, 'Admin/login_page.html', {'pass_error': 'Incorrect Password'})
        elif user == 'student':
            users = Student.objects.all()
            for u in users:
                if u.emailAdd == username1:

                    if decrypt(u.password) == password1:
                        user = authenticate(request, username=username1, password=password1)
                        print(user)
                        if user == None:
                            User.objects.create_user(username=username1, password=password1)
                            user = authenticate(request, username=username1, password=password1)
                        print(user)
                        if user is not None:
                            login(request,user)
                        role = 'student'
                        params = {'username': username1,'role': role}
                        return render(request,'student/student_homepage.html', params)
                    else:
                        print(password1)
                        return render(request, 'Admin/login_page.html', {'pass_error': 'Incorrect Password'})
        elif user== 'pending':
            return render(request, 'Admin/login_page.html', {'email_error': 'Your Email is not Yet Verified by the college.'})

    else:
        return render(request, 'Admin/login_page.html', {'email_error': 'Invalid Email'})


def register_success(request):

    fname=request.POST.get('fname')

    mname=request.POST.get('mname')
    lname=request.POST.get('lname')
    mobno=request.POST.get('mobno')
    email=request.POST.get('email')
    password=request.POST.get('password')
    en_password=encrypt(password)
    clg=request.POST.get('clg')
    colid=request.POST.get('colid')
    degree=request.POST.get('degree')
    yoc=request.POST.get('yoc')
    work=request.POST.get('work')
    anninc=request.POST.get('anninc')
    address=request.POST.get('address')
    pincode=request.POST.get('pincode')
    gender=request.POST.get('gender')
    dept=request.POST.get('dept')
    file1 = request.FILES['filed']
    fs = FileSystemStorage()
    filename = fs.save(file1.name, file1)
    image_url = fs.url(filename)
    std=Student(firstName=fname,middleName=mname,lastName=lname,mobileNo=mobno,password=en_password,emailAdd=email,collegeAdmissionId=colid,currentWorkStatus=work,AnnualIncome=anninc,address=address,pincode=pincode,gender=gender,degreePersuedFromClg=degree,YearOfCompletion=yoc,CollegeName=clg,department=dept,image=image_url,verificationStatus='inaction')
    std.save()
    u_data=User_data(emailAdd=email,role='pending')
    u_data.save()
    college=College.objects.filter(collegeName=clg)
    eml=college[0].emailAdd



    try:

        # msg = MIMEMultipart()
        msg=EmailMessage()
        msg.set_content("New request for alumini arrives\n please verify the alumni")
        msg['From'] = settings.EMAIL_ADDRESS
        msg['To'] = eml
        msg['Subject'] = "New Alumni Request"
        server=smtplib.SMTP_SSL('smtp.gmail.com',465)

        server.login(settings.EMAIL_ADDRESS,settings.EMAIL_PASSWORD)
        server.send_message(msg)

        server.quit()
    except:
        print('not success')
    return render(request,'Admin/homepage.html')

@login_required()
@csrf_exempt
def change_password(request):
    role = request.GET.get('role')
    username = request.GET.get('username')
    if role == 'student':
        param = {'username': username, 'role': role}
        return render(request,'student/update_student_password.html', param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
@csrf_exempt
def change_student_password(request):
    role = request.POST.get('role')
    if role == 'student':
        username = request.POST.get('username')
        cur_pass = request.POST.get('curpass')

        clg = Student.objects.filter(emailAdd=username)
        de_pass = decrypt(clg[0].password)
        if de_pass == cur_pass:
            new_pass = request.POST.get('newpass')
            en_newpass = encrypt(new_pass)
            Student.objects.filter(emailAdd=username).update(password=en_newpass)
            user = authenticate(request, username=username, password=new_pass)
            print(user)
            if user == None:
                User.objects.get(username=username).delete()
                User.objects.create_user(username=username, password=new_pass)
                user = authenticate(request, username=username, password=new_pass)
                print(user)
            if user is not None:
                login(request, user)

            student = Student.objects.filter(emailAdd=username)
            param = {'role': role, 'username': username, 'student': student[0]}
            return render(request, 'student/student_homepage.html', param)
        else:
            params = {'username': username, 'role': role, 'pass_err': 'wrong password'}
            return render(request, 'student/update_student_password.html', params)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
@csrf_exempt
def change_image(request):
    role = request.GET.get("role")
    username = request.GET.get("username")
    if role == 'student':
        student = Student.objects.filter(emailAdd=username)
        param = {'role': role, 'username': username, 'student': student[0]}
        return render(request, 'student/update_student_image.html', param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
@csrf_exempt
def after_image_update(request):
    role = request.POST.get('role')
    username = request.POST.get('username')
    file1 = request.FILES['clgimage']
    fs = FileSystemStorage()
    filename = fs.save(file1.name, file1)
    image_url ='/media/'+filename
    if role == 'student':
        student = Student.objects.filter(emailAdd=username)
        student.update(image=image_url)
        student = Student.objects.filter(emailAdd=username)
        param = {'role': role, 'username': username, 'student': student[0]}
        return render(request, 'student/student_homepage.html', param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def view_student_profile(request):
    role = request.GET.get('role')
    username = request.GET.get('username')
    if role == 'student':
        student = Student.objects.filter(emailAdd=username)
        param = {'student': student[0], 'role': role, 'username': username}
        return render(request, 'student/view_student_profile.html', param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def update_student(request):
    role = request.POST.get('role')
    username = request.POST.get('username')
    if role == 'student':
        student = Student.objects.filter(emailAdd=username)
        depts = ['CSE', 'IT', 'CIVIL', 'MECH', 'ETC']
        sts = ['Job', 'Buissness', 'Yet to be placed', 'Startup', 'Others']
        param = {'student': student[0], 'role': role, 'username': username, 'depts': depts,'sts':sts}
        return render(request, 'student/update_student.html', param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def update_student_profile(request):
    role = request.POST.get('role')
    username = request.POST.get("student_old_username")
    if role == 'student':
        fname = request.POST.get('fname')
        mname = request.POST.get('mname')
        lname = request.POST.get('lname')
        mobno = request.POST.get('mobno')
        email = request.POST.get('email')
        anninc = request.POST.get('anninc')
        work = request.POST.get('work')

        address = request.POST.get('address')

        pin = request.POST.get('pin')
        gender = request.POST.get('gender')

        student = Student.objects.filter(emailAdd=username)
        student.update(firstName=fname, middleName=mname, lastName=lname, mobileNo=mobno, emailAdd=email,
                        address=address, pincode=pin,AnnualIncome=anninc, currentWorkStatus=work, gender=gender)
        User_data.objects.filter(emailAdd=username).update(emailAdd=email)
        username = email
        student = Student.objects.filter(emailAdd=email)
        param = {'student': student[0], 'role': role, 'username': username}
        return render(request, 'student/student_homepage.html', param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')


def validate_email(request):
    email=request.POST.get('email',None)
    print(email)
    data = {
        'is_taken':User_data.objects.filter(emailAdd=email).exists()
    }
    return JsonResponse(data)

@login_required()
def view_college_info(request):
    role = request.GET.get('role')
    username = request.GET.get('username')
    if role == 'student':
        clgs = College.objects.all()
        params = {'colleges': clgs, 'role': role, 'username': username}
        return render(request, 'student/view_all_colleges.html', params)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def view_full_college_info(request):
    role = request.GET.get('role')
    username = request.GET.get('username')
    if role=='student':
        id = request.GET.get('clgid')
        clg = College.objects.filter(id=id)
        courses = clg[0].coursesOffered.split("!")
        departments = clg[0].departments.split("!")
        param = {'college': clg[0], 'role': role,'username':username, 'departments': departments, 'courses': courses}
        return render(request, 'student/college_full_info.html', param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

def upvote_consensus(request):
    email = request.POST.get('email', None)
    student=Student.objects.filter(emailAdd=email)
    print(email)
    voteid=request.POST.get('voteid')
    review=Consensus.objects.get(id=voteid)
    taken=review.votes.exists(student[0].id)
    if(not taken):
        review.votes.up(student[0].id)
        count=review.votes.count()
        print(count)
    if(taken):
        review.votes.down(student[0].id)
        count = review.votes.count()
        print(count)

    data = {
        'is_taken':review.votes.exists(student[0].id)
    }
    return JsonResponse(data)

@login_required()
def view_consensus(request):
    role=request.GET.get('role')
    if role=='student':
        username=request.GET.get('username')
        student=Student.objects.filter(emailAdd=username)
        clg=student[0].CollegeName
        articles=Consensus.objects.filter(collegeName=clg).order_by('-dateOfPublish')
        l=[]
        for article in articles:
            review=Consensus.objects.get(id=article.id)
            if review.votes.exists(student[0].id):
               t=[article.id,'yes']
               l.append(t)
            else:
                t =[article.id,'no']
                l.append(t)

        param={'role':role,'username':username,'articles':articles,'d':l}
        return render(request,'student/view_consensus.html',param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')


@login_required()
def view_notices(request):
    role=request.GET.get('role')
    if role=='student':
        username=request.GET.get('username')
        std=Student.objects.filter(emailAdd=username)
        clg=std[0].CollegeName
        college=College.objects.filter(collegeName=clg)
        notices = Notice.objects.filter(emailAdd=college[0].emailAdd).order_by("-dateOfPublish")
        param = {'role': role, 'username': username, 'notices': notices}
        return render(request, 'student/notices.html', param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def view_full_notices(request):
    role = request.GET.get('role')
    if role == 'student':
        username = request.GET.get('username')
        id=request.GET.get('noticeid')
        notice=Notice.objects.filter(id=id)
        param={'username':username,'role':role,'notice':notice[0]}
        return render(request,'student/full_notice.html',param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

def after_forget_password(request):
    return render(request,'student/forget_password.html')

def forgot_email_pass(request):
    email=request.GET.get('eml')
    if User_data.objects.filter(emailAdd=email).exists():
        user=User_data.objects.filter(emailAdd=email)
        if (user[0].role=='admin'):
            pwd=Admin.objects.filter(emailAdd=email)[0].password
        elif (user[0].role == 'student'):
            pwd = Student.objects.filter(emailAdd=email)[0].password
        elif (user[0].role == 'college'):
            pwd = College.objects.filter(emailAdd=email)[0].password

        pwd=pwd[5:30:2]
        try:
                msg = EmailMessage()
                msg.set_content("Here is your password reset code \n\n" + pwd +
                                "\n\nPlease enter the above code to reset your password ")
                msg['From'] = settings.EMAIL_ADDRESS
                msg['To'] = email
                msg['Subject'] = "Password Reset"
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

                server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
                server.send_message(msg)

                server.quit()
        except:
                print('not success')
        return render(request,'student/password_reset_email_verification.html',{'pwd':pwd,'username':email})
    else:
        return render(request, 'student/forget_password.html',{'eml_error':'Invalid Email'})
@csrf_exempt
def verify_code(request):
    code=request.POST.get('pwdrst')
    pwd=request.POST.get('pwd')
    username=request.POST.get('username')
    print(username)
    if code==pwd:
        return render(request,'student/reset_password.html',{'username':username})
    else:
        return render(request,'student/password_reset_email_verification.html', {'pwd': pwd,'username':username,'error_data':'Invalid code'})

@csrf_exempt
def reset_password(request):
    username=request.POST.get('username')
    newpwd=request.POST.get('newpass')
    user = User_data.objects.filter(emailAdd=username)
    if (user[0].role == 'admin'):
        Admin.objects.filter(emailAdd=username).update(password=encrypt(newpwd))
    elif (user[0].role == 'student'):
        Student.objects.filter(emailAdd=username).update(password=encrypt(newpwd))
    elif (user[0].role == 'college'):
        College.objects.filter(emailAdd=username).update(password=encrypt(newpwd))
    return render(request,'Admin/login_page.html')
