from django.shortcuts import render,redirect
from django.http import HttpResponse
from college.models import College,Consensus,Notice
from student.views import encrypt,decrypt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import User_data
from .models import Admin
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from student.models import Student
# Create your views here.

@login_required()
@csrf_exempt
def admin_homepage(request):
    role = request.GET.get('role')
    username = request.GET.get('username')
    if role=='admin':
        param={'username':username,'role':role}
        return render(request,'Admin/admin_homepage.html',param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')


@csrf_exempt
def login_here(request):
    return render(request,'Admin/login_page.html')


@login_required()
def register_college(request):
    role=request.GET.get('role')
    username=request.GET.get('username')
    if role=='admin':
        courses=['B.tech', 'B.E.', 'MBA', 'LAW', 'ARTS', 'MEDICAL']
        depts=['CSE','IT','CIVIL','MECH','ETC']
        return render(request,'Admin/college_registration.html',{'role':'admin','username':username,'courses':courses,'department':depts})
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def college_register_sucess(request):
    role = request.POST.get('role')
    if role == 'admin':
        username = request.POST.get('username')
        if request.method == 'POST':
                clgname = request.POST.get('clgname')
                mobno = request.POST.get('mobno')
                email = request.POST.get('email')
                password = request.POST.get('password')
                en_password=encrypt(password)
                clgtype = request.POST.get('coltype')
                clgid = request.POST.get('colid')
                depts = "!".join(request.POST.getlist('depts'))
                yoe = request.POST.get('yoe')
                crs = "!".join(request.POST.getlist('courses'))
                unv = request.POST.get('unv')
                address = request.POST.get('address')
                pincode = request.POST.get('pincode')
                principle=request.POST.get('principle')
                form=College(collegeName=clgname,collegeType=clgtype,collegeId=clgid,coursesOffered=crs,departments=depts,mobileNo =mobno,password=en_password,emailAdd=email,address=address,pincode=pincode,university=unv,yearOfEstablishment=yoe,principleName=principle)
                form.save()
                print('valid')
                form1=User_data(emailAdd=email,role='college')
                form1.save()
        else:
                print('invalid')
        return render(request, 'Admin/admin_homepage.html', {'username': username, 'role': role})
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def view_colleges(request):
    role = request.GET.get('role')
    if role=='admin':
        username=request.GET.get('username')
        clgs = College.objects.all()
        params = {'colleges': clgs,'role':role,'username':username}
        return render(request, 'Admin/view_colleges.html', params)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def view_full_info(request):
    role = request.GET.get('role')
    username=request.GET.get('username')
    if role=='admin':
        id=request.GET.get('clgid')
        clg=College.objects.filter(id=id)
        courses=clg[0].coursesOffered.split("!")
        departments=clg[0].departments.split("!")
        param={'college':clg[0],'role':role,'departments':departments,'courses':courses,'username':username}
        return render(request,'Admin/college_full_info.html',param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def change_password(request):
    role = request.GET.get('role')
    username = request.GET.get('username')
    if role == 'admin':
        param = {'username': username, 'role': role}
        return render(request,'admin/update_admin_password.html', param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
@csrf_exempt
def change_admin_password(request):
    role = request.POST.get('role')
    if role == 'admin':
        username = request.POST.get('username')
        cur_pass = request.POST.get('curpass')

        clg = Admin.objects.filter(emailAdd=username)
        de_pass = decrypt(clg[0].password)
        if de_pass == cur_pass:
            new_pass = request.POST.get('newpass')
            en_newpass = encrypt(new_pass)
            Admin.objects.filter(emailAdd=username).update(password=en_newpass)
            user = authenticate(request, username=username, password=new_pass)
            print(user)
            if user == None:
                User.objects.get(username=username).delete()
                User.objects.create_user(username=username, password=new_pass)
                user = authenticate(request, username=username, password=new_pass)
                print(user)
            if user is not None:
                login(request, user)

            admin = Admin.objects.filter(emailAdd=username)
            param = {'role': role, 'username': username, 'admin': admin[0]}
            return render(request, 'admin/admin_homepage.html', param)
        else:
            params = {'username': username, 'role': role, 'pass_err': 'wrong password'}
            return render(request, 'admin/update_admin_password.html', params)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def view_admin_profile(request):
    role=request.GET.get('role')
    username=request.GET.get('username')
    if role=='admin':
            admin=Admin.objects.filter(emailAdd=username)

            param = {'admin': admin[0], 'role': role, 'username': username}
            return render(request, 'admin/show_admin_profile.html', param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def update_admin(request):
    role = request.GET.get('role')
    username = request.GET.get('username')
    if role == 'admin':
        admin = Admin.objects.filter(emailAdd=username)
        param = {'admin': admin[0], 'role': role, 'username': username}
        return render(request, 'admin/update_admin_profile.html', param)

    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
@csrf_exempt
def update_admin_profile(request):
    role = request.POST.get('role')
    username = request.POST.get("student_old_username")
    if role == 'admin':
        fname = request.POST.get('fname')
        mname = request.POST.get('mname')
        lname = request.POST.get('lname')
        mobno = request.POST.get('mobno')
        email = request.POST.get('email')
        address = request.POST.get('address')
        pin = request.POST.get('pin')
        age = request.POST.get('age')

        admin = Admin.objects.filter(emailAdd=username)
        admin.update(firstName=fname, middleName=mname, lastName=lname, mobileNo=mobno, emailAdd=email,
                        address=address, pincode=pin, age=age)
        User_data.objects.filter(emailAdd=username).update(emailAdd=email)
        username = email
        admin = Admin.objects.filter(emailAdd=email)
        param = {'admin': admin[0], 'role': role, 'username': username}
        return render(request, 'admin/admin_homepage.html', param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
@csrf_exempt
def user_logout(request):
    username=request.GET.get('username')
    logout(request)
    try:
        User.objects.get(username=username).delete()
    except:
        print('already logged out')
    return redirect("/")

@login_required()
def delete_college(request):
    role=request.GET.get('role')
    if role=='admin':
        username=request.GET.get('username')
        clgid=request.GET.get('clgid')
        clg=College.objects.filter(id=clgid)
        if Consensus.objects.filter(emailAdd=clg[0].emailAdd).exists():
            Consensus.objects.filter(emailAdd=clg[0].emailAdd).delete()
        if Notice.objects.filter(emailAdd=clg[0].emailAdd).exists():
            Notice.objects.filter(emailAdd=clg[0].emailAdd).delete()

        User_data.objects.filter(emailAdd=clg[0].emailAdd).delete()
        Student.objects.filter(CollegeName=clg[0].collegeName).delete()
        College.objects.filter(id=clgid).delete()
        clgs = College.objects.all()
        params = {'colleges': clgs, 'role': role, 'username': username}
        return render(request, 'Admin/view_colleges.html', params)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')