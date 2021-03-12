from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Student(models.Model):
    firstName = models.CharField(max_length=30, default=None)
    middleName = models.CharField(max_length=30, null=True, blank=True)
    lastName = models.CharField(max_length=30, default=None)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message=(
                                     "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    mobileNo = models.CharField(validators=[phone_regex], max_length=15)
    password = models.CharField(max_length=500, default=None)
    emailAdd = models.EmailField(max_length=40, default=None,unique=True)
    collegeAdmissionId=models.CharField(max_length=300,default=None)
    currentWorkStatus=models.CharField(max_length=300,default=None)
    AnnualIncome=models.IntegerField(max_length=100,null=True,blank=True)
    address = models.TextField(max_length=300, default=None)
    pincode = models.IntegerField(default=None)
    gender = models.CharField(max_length=15, default=None)
    degreePersuedFromClg=models.CharField(max_length=100,default=None)
    YearOfCompletion=models.CharField(max_length=10,default=None)
    CollegeName=models.CharField(max_length=200,default=None)
    department=models.CharField(max_length=100,default=None)
    verificationStatus=models.CharField(max_length=50)
    image = models.ImageField(upload_to='Student/media', default='College/media/default.jpg')

    def __str__(self):
        return self.emailAdd

    class Meta:
        db_table="Alumini Info"






