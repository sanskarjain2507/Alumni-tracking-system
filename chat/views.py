# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
from Admin.models import User_data,Admin
from student.models import Student
from college.models import College
import json

def index(request):
    return render(request, 'chat/index.html', {})

# @login_required
def room(request, room_name):
    username=request.user.username
    role=User_data.objects.filter(emailAdd=username)[0]
    role=role.role
    if role=='college':
        usr=College.objects.filter(emailAdd=username)[0]
    elif role=='student':
        usr=Student.objects.filter(emailAdd=username)[0]
    if role=='admin':
        usr=Admin.objects.filter(emailAdd=username)[0]
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username':mark_safe(json.dumps(request.user.username)),
        'usr':usr
    })