from django.db import models
from vote.models import VoteModel
from django.core.validators import RegexValidator
# Create your models here.
class College(models.Model):
    collegeName=models.CharField(max_length=200,default=None)
    collegeType=models.CharField(max_length=200)
    collegeId=models.CharField(max_length=200,unique=True)
    coursesOffered=models.CharField(max_length=500)
    departments=models.CharField(max_length=500)
    principleName=models.CharField(max_length=100)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message=(
                                     "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    mobileNo = models.CharField(validators=[phone_regex], max_length=15)
    password = models.CharField(max_length=500, default=None)
    emailAdd = models.EmailField(max_length=40, default=None, unique=True)
    address = models.TextField(max_length=300, default=None)
    pincode = models.IntegerField(default=None)
    university=models.CharField(default=None,max_length=200)
    yearOfEstablishment=models.CharField(default=None,max_length=10)
    image = models.ImageField(upload_to='College/media',default='College/media/default.jpg')
    def  __str__(self):
        return self.emailAdd

    class Meta:
        db_table="College Information"

class Consensus(VoteModel,models.Model):
    article=models.CharField(max_length=1000,default=None)
    emailAdd = models.EmailField(max_length=40, default=None)
    collegeName=models.CharField(max_length=1000)
    dateOfPublish=models.DateTimeField(auto_now_add=True)

class Notice(models.Model):
    noticeTitle=models.CharField(max_length=1000,default=None)
    noticeBody=models.CharField(max_length=10000,default=None)
    emailAdd = models.EmailField(max_length=40, default=None)
    collegeName = models.CharField(max_length=1000)
    dateOfPublish = models.DateTimeField(auto_now_add=True)
