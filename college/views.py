from django.shortcuts import render,redirect
from .models import College,Consensus,Notice
from django.core.files.storage import FileSystemStorage
from Admin.models import User_data
from django.contrib.auth.models import User
from student.views import encrypt,decrypt
from django.contrib.auth import authenticate,login,logout
from student.models import Student
from email.message import EmailMessage
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import smtplib

@login_required()
def college_homepage(request):
    role = request.GET.get("role")
    username = request.GET.get("username")
    if role == 'college':
        college = College.objects.filter(emailAdd=username)
        param = {'role': role, 'username': username, 'college': college[0]}
        return render(request, 'college/college_homepage.html', param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def change_image(request):
    role = request.GET.get("role")
    username = request.GET.get("username")
    if role == 'college':
        college = College.objects.filter(emailAdd=username)
        param = {'role': role, 'username': username, 'college': college[0]}
        return render(request, 'college/update_profile_image.html', param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def after_image_update(request):
    role=request.POST.get('role')
    username=request.POST.get('username')
    file1 = request.FILES['clgimage']
    fs = FileSystemStorage()
    filename = fs.save(file1.name, file1)
    image_url ='/media/'+filename
    if role=='college':
        college = College.objects.filter(emailAdd=username)
        college.update(image=image_url)
        college = College.objects.filter(emailAdd=username)
        param = {'role': role, 'username': username, 'college': college[0]}
        return render(request,'college/college_homepage.html',param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def view_colleges(request):
    role = request.GET.get('role')
    username = request.GET.get('username')
    if role=='college':
        clgs = College.objects.all()
        params = {'colleges': clgs, 'role': role,'username':username}
        return render(request, 'college/view_all_colleges.html', params)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def view_college_info(request):
    role = request.GET.get('role')
    username = request.GET.get('username')
    if role=='college':
        id = request.GET.get('clgid')
        clg = College.objects.filter(id=id)
        courses = clg[0].coursesOffered.split("!")
        departments = clg[0].departments.split("!")
        param = {'college': clg[0], 'role': role,'username':username, 'departments': departments, 'courses': courses}
        return render(request, 'college/college_full_info.html', param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def view_profile(request):
        role=request.GET.get('role')
        username=request.GET.get('username')
        if role=='college':
            clg=College.objects.filter(emailAdd=username)
            courses = clg[0].coursesOffered.split("!")
            departments = clg[0].departments.split("!")
            param = {'clg': clg[0], 'role': role, 'username': username, 'departments': departments,'courses': courses}
            return render(request, 'college/college_profile.html', param)
        else:
            return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')
@login_required()
def update_college(request):
    role=request.POST.get('role')
    username=request.POST.get('username')
    if role == 'college':
        clg = College.objects.filter(emailAdd=username)
        courses = clg[0].coursesOffered.split("!")
        departments = clg[0].departments.split("!")
        crs = ['B.tech', 'B.E.', 'MBA', 'LAW', 'ARTS', 'MEDICAL']
        depts = ['CSE', 'IT', 'CIVIL', 'MECH', 'ETC']
        param = {'clg': clg[0], 'role': role, 'username': username,'depts':depts,'crs':crs, 'departments': departments, 'courses': courses}
        return render(request, 'college/update_college.html', param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def update_college_profile(request):
    role=request.POST.get('role')
    username=request.POST.get("college_old_username")
    if role=='college':
        clgname = request.POST.get('name')
        mobno = request.POST.get('mobno')
        email = request.POST.get('email')
        clgtype = request.POST.get('clgtype')
        clgid = request.POST.get('collegeId')
        depts = "!".join(request.POST.getlist('ndepts'))
        yoe = request.POST.get('yoe')
        crs = "!".join(request.POST.getlist('ncourses'))
        unv = request.POST.get('unv')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        principle = request.POST.get('prinName')
        college = College.objects.filter(emailAdd=username)
        college.update(collegeName=clgname, collegeType=clgtype, collegeId=clgid, coursesOffered=crs, departments=depts,
                       mobileNo=mobno, emailAdd=email, address=address, pincode=pincode,
                       university=unv, yearOfEstablishment=yoe, principleName=principle)
        User_data.objects.filter(emailAdd=username).update(emailAdd=email)
        username=email
        clg=College.objects.filter(emailAdd=email)
        param = {'college': clg[0], 'role': role, 'username': username}
        return render(request, 'college/college_homepage.html', param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def change_password(request):
    role=request.GET.get('role')
    username=request.GET.get('username')
    if role=='college':
        param = {'username': username, 'role': role}
        return render(request,'college/update_college_password.html',param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def change_college_password(request):
    role = request.POST.get('role')
    if role == 'college':
        username = request.POST.get('username')
        cur_pass = request.POST.get('curpass')

        clg = College.objects.filter(emailAdd=username)
        de_pass = decrypt(clg[0].password)
        if de_pass == cur_pass:
            new_pass = request.POST.get('newpass')
            en_newpass = encrypt(new_pass)
            College.objects.filter(emailAdd=username).update(password=en_newpass)
            user = authenticate(request, username=username, password=new_pass)
            print(user)
            if user == None:
                User.objects.get(username=username).delete()
                User.objects.create_user(username=username, password=new_pass)
                user = authenticate(request, username=username, password=new_pass)
                print(user)
            if user is not None:
                login(request, user)

            college = College.objects.filter(emailAdd=username)
            param = {'role': role, 'username': username, 'college': college[0]}
            return render(request, 'college/college_homepage.html', param)
        else:
            params = {'username': username, 'role': role, 'pass_err': 'wrong password'}
            return render(request, 'college/update_college_password.html', params)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def view_alumini_request(request):
    role=request.GET.get('role')
    username=request.GET.get('username')
    if role=='college':
        clg=College.objects.filter(emailAdd=username)
        student=Student.objects.filter(CollegeName=clg[0].collegeName,verificationStatus='inaction')
        param = {'college': clg[0], 'role': role, 'username': username,'alumnis': student}
        return render(request,'college/verify_alumini.html',param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def verify_alumini(request):
    role = request.GET.get('role')
    username = request.GET.get('username')
    if role=='college':
        clg=College.objects.filter(emailAdd=username)
        id=request.GET.get('clgid')
        student=Student.objects.filter(id=id)
        student.update(verificationStatus='active')
        User_data.objects.filter(emailAdd=student[0].emailAdd).update(role='student')
        try:

            # msg = MIMEMultipart()
            msg = EmailMessage()
            msg.set_content(f"Congratulation your verification has been approved by {clg[0].collegeName} \n You can now login to the website")
            msg['From'] = settings.EMAIL_ADDRESS
            msg['To'] = student[0].emailAdd
            msg['Subject'] = "Alumini Request Verified"
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

            server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
            server.send_message(msg)

            server.quit()
        except:
            print('not success')
        student = Student.objects.filter(CollegeName=clg[0].collegeName, verificationStatus='inaction')
        param = {'college': clg[0], 'role': role, 'username': username, 'alumnis': student}
        return render(request, 'college/verify_alumini.html', param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def discard_alumini(request):
    role = request.GET.get('role')
    username = request.GET.get('username')
    if role=='college':
        clg=College.objects.filter(emailAdd=username)
        id=request.GET.get('clgid')
        student=Student.objects.filter(id=id)


        User_data.objects.filter(emailAdd=student[0].emailAdd).delete()
        try:

            # msg = MIMEMultipart()
            msg = EmailMessage()
            msg.set_content(f"Sorry your verification has been rejected by {clg[0].collegeName} \n You can try again")
            msg['From'] = settings.EMAIL_ADDRESS
            msg['To'] = student[0].emailAdd
            msg['Subject'] = "Alumini Request Not Verified"
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

            server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
            server.send_message(msg)

            server.quit()
        except:
            print('not success')
        Student.objects.filter(id=id).delete()
        student = Student.objects.filter(CollegeName=clg[0].collegeName, verificationStatus='inaction')
        param = {'college': clg[0], 'role': role, 'username': username, 'alumnis': student}
        return render(request, 'college/verify_alumini.html', param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def view_alumni_info(request):
    role=request.GET.get('role')
    username=request.GET.get('username')
    if role=='college':
        id=request.GET.get('stdid')
        student=Student.objects.filter(id=id)
        param = {'student': student[0], 'role': role, 'username': username}
        return render(request,'college/alumini_full_info.html',param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def view_location(request):
    return render(request,'college/view_alumnis_location.html')


def validate_college_id(request):
    clgid = request.POST.get('clgid', None)

    print(clgid)
    data = {
        'is_taken': College.objects.filter(collegeId=clgid).exists()

    }
    return JsonResponse(data)

@login_required()
def publish_consensus(request):
    role=request.GET.get('role')
    if role=='college':
        username=request.GET.get('username')
        param={'role':role,'username':username}
        return render(request,'college/create_consensus.html',param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def submit_consensus(request):
    role=request.POST.get('role')
    if role=='college':
        username=request.POST.get('username')
        question=request.POST.get('voteText')
        college=College.objects.filter(emailAdd=username)
        consensus=Consensus(article=question,emailAdd=username,collegeName=college[0].collegeName)
        consensus.save()
        param={'role':role,'username':username}
        return render(request,'college/college_homepage.html',param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def view_consensus(request):
    role=request.GET.get('role')
    if role=='college':
        username=request.GET.get('username')
        all_votes=Consensus.objects.filter(emailAdd=username).order_by('-dateOfPublish')
        param={'role':role,'username':username,'votes':all_votes}
        return render(request,'college/view_consensus.html',param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def view_consensus_info(request):
    role=request.GET.get('role')
    if role=='college':
        username=request.GET.get('username')
        voteid=request.GET.get('voteid')
        article=Consensus.objects.get(id=voteid)
        count=article.votes.count()
        user_ids=article.votes.user_ids()
        l=[]
        for i in user_ids:
            s=Student.objects.filter(id=i[0])[0]
            l.append(s.emailAdd)

        param={'role':role,'username':username,'students':l,'count':count,'article':article}
        return render(request,'college/view_consensus_full_info.html',param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
@csrf_exempt
def publish_notice(request):
    role=request.GET.get('role')
    if role=='college':
        username=request.GET.get('username')
        param={'username':username,'role':role}
        return render(request,'college/post_notice.html',param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
@csrf_exempt
def send_notice(request):
    role = request.POST.get('role')
    if role == 'college':
        username = request.POST.get('username')
        ntitle=request.POST.get('notice')
        nbody=request.POST.get('nbody')
        college=College.objects.filter(emailAdd=username)
        clg=college[0].collegeName
        notice=Notice(noticeTitle=ntitle,noticeBody=nbody,emailAdd=username,collegeName=clg)
        notice.save()
        param={'username':username,'role':role}
        return render(request,'college/college_homepage.html',param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
@csrf_exempt
def view_notices(request):
    role=request.GET.get('role')
    if role=='college':
        username=request.GET.get('username')
        notices=Notice.objects.filter(emailAdd=username).order_by("-dateOfPublish")
        param={'role':role,'username':username,'notices':notices}
        return render(request,'college/view_notice.html',param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def view_full_notice(request):
    role = request.GET.get('role')
    if role == 'college':
        username = request.GET.get('username')
        id=request.GET.get('noticeid')
        notice=Notice.objects.filter(id=id)
        param={'username':username,'role':role,'notice':notice[0]}
        return render(request,'college/full_notice.html',param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def delete_notice(request):
    role=request.GET.get('role')
    if role=='college':
        username=request.GET.get('username')
        id=request.GET.get('noticeid')
        Notice.objects.filter(id=id).delete();
        notices = Notice.objects.filter(emailAdd=username).order_by("-dateOfPublish")
        param = {'role': role, 'username': username, 'notices': notices}
        return render(request, 'college/view_notice.html', param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def delete_consensus(request):
    role=request.GET.get('role')
    if role=='college':
        username=request.GET.get('username')
        id=request.GET.get('voteid')
        Consensus.objects.filter(id=id).delete()
        all_votes = Consensus.objects.filter(emailAdd=username).order_by('-dateOfPublish')
        param = {'role': role, 'username': username, 'votes': all_votes}
        return render(request, 'college/view_consensus.html', param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def view_alumnis(request):
    role=request.GET.get('role')
    if role=='college':
        username = request.GET.get('username')
        clg=College.objects.filter(emailAdd=username)[0]
        alumnis=Student.objects.filter(CollegeName=clg.collegeName).order_by('-AnnualIncome')
        depts = ['CSE', 'IT', 'CIVIL', 'MECH', 'ETC']
        courses=['B.tech', 'B.E.', 'MBA', 'LAW', 'ARTS', 'MEDICAL']
        param={'role':role,'username':username,'depts':depts,'courses':courses,'alumnis':alumnis}
        return render(request,'college/view_alumnis.html',param)
    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')

@login_required()
def group_chat(request):
    role=request.GET.get('role')
    if role=='college':
        username=request.GET.get('username')
        clg=College.objects.filter(emailAdd=username)[0]
        grp=clg.collegeName.split(" ")
        g=''
        for i in grp:
            if i.isalnum():
                g+=i
        param={'username':username,'role':role,'clgname':clg.collegeName}
        return redirect('/chat/'+g)

@login_required()
def full_alumni_info(request):
    role=request.GET.get('role')
    if role=='college':
        username=request.GET.get('username')
        id=request.GET.get('almid')
        alumni=Student.objects.filter(id=id)[0]
        param={'username':username,'role':role,'student':alumni}
        return render(request,'college/alumini_full_info.html',param)

def alumni_search(request):
    role = request.GET.get('role')
    print(role)
    if role == 'college':
        username = request.GET.get('username')
        search_by = request.GET.get('sel_cr')
        depts = ['CSE', 'IT', 'CIVIL', 'MECH', 'ETC']
        courses = ['B.tech', 'B.E.', 'MBA', 'LAW', 'ARTS', 'MEDICAL']
        clg = College.objects.filter(emailAdd=username)[0]
        print(search_by)
        if (search_by == 'selection_criteria'):
            alumnis = Student.objects.filter(CollegeName=clg.collegeName).order_by('-AnnualIncome')
            param = {'role': role, 'username': username, 'depts': depts, 'courses': courses, 'alumnis': alumnis}
        elif (search_by == 'department'):
            search_for = request.GET.get('dept_sel')

            search_available = Student.objects.filter(CollegeName=clg.collegeName,department=search_for).exists()
            if search_available != False:
                alumnis = Student.objects.filter(CollegeName=clg.collegeName, department=search_for).order_by(
                    '-AnnualIncome')
                param = {'role': role, 'username': username, 'depts': depts, 'courses': courses, 'alumnis': alumnis}
            else:
                param = {'username': username, 'empty_condition': "NO RESULT MATCHES YOU SEARCH", 'role': role,
                         'depts': depts, 'courses': courses}
        elif (search_by == 'year'):
            search_for=request.GET.get('srch')

            search_available = Student.objects.filter(CollegeName=clg.collegeName,YearOfCompletion=search_for).exists()
            if search_available != False:
                alumnis = Student.objects.filter(CollegeName=clg.collegeName,YearOfCompletion=search_for).order_by('-AnnualIncome')
                param = {'role': role, 'username': username, 'depts': depts, 'courses': courses, 'alumnis': alumnis}
            else:
                param = {'username': username, 'empty_condition': "NO RESULT MATCHES YOU SEARCH", 'role': role,'depts':depts,'courses':courses}
        elif search_by == 'min_sal':
            search_for=int(request.GET.get('srch'))
            search_available = Student.objects.filter(CollegeName=clg.collegeName,AnnualIncome__gte=search_for).exists()

            if search_available != False:
                alumnis = Student.objects.filter(CollegeName=clg.collegeName, AnnualIncome__gte=search_for)
                param = {'role': role, 'username': username, 'depts': depts, 'courses': courses, 'alumnis': alumnis}
            else:
                param = {'username': username, 'empty_condition': "NO RESULT MATCHES YOU SEARCH", 'role': role,'depts':depts,'courses':courses}
        elif search_by == 'max_sal':
            search_for = int(request.GET.get('srch'))
            search_available = Student.objects.filter(CollegeName=clg.collegeName,
                                                      AnnualIncome__lte=search_for).exists()

            if search_available != False:
                alumnis = Student.objects.filter(CollegeName=clg.collegeName, AnnualIncome__lte=search_for)
                param = {'role': role, 'username': username, 'depts': depts, 'courses': courses, 'alumnis': alumnis}
            else:
                param = {'username': username, 'empty_condition': "NO RESULT MATCHES YOU SEARCH", 'role': role,
                          'depts': depts, 'courses': courses}
        return render(request,'college/view_alumnis.html',param)

    else:
        return HttpResponse('<center><h1>ACCESS DENIED!!</h1></center>')
