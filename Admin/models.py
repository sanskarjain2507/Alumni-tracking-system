from django.db import models
from django.core.validators import RegexValidator
# Create your models here.

class Admin(models.Model):
    firstName = models.CharField(max_length=30, default=None)
    middleName = models.CharField(max_length=30, null=True, blank=True)
    lastName = models.CharField(max_length=30, default=None)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message=(
                                     "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    mobileNo = models.CharField(validators=[phone_regex], max_length=15)
    password = models.CharField(max_length=500, default=None)
    emailAdd = models.EmailField(max_length=40, default=None)
    age = models.IntegerField(default=None)
    address = models.TextField(max_length=300, default=None)
    pincode = models.IntegerField(default=None)

    def __str__(self):
        return self.emailAdd

    class Meta:
        db_table="Admin information"

class User_data(models.Model):
    emailAdd=models.EmailField(max_length=40,default=None,unique=True)
    role=models.CharField(max_length=40,default=None)

    class Meta:
        db_table="Login Info"