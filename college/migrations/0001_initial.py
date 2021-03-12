# Generated by Django 3.0.2 on 2020-01-12 10:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collegeName', models.CharField(default=None, max_length=200)),
                ('collegeType', models.CharField(max_length=200)),
                ('collegeId', models.CharField(max_length=200, unique=True)),
                ('coursesOffered', models.CharField(max_length=500)),
                ('departments', models.CharField(max_length=500)),
                ('principleName', models.CharField(max_length=100)),
                ('mobileNo', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('password', models.CharField(default=None, max_length=500)),
                ('emailAdd', models.EmailField(default=None, max_length=40, unique=True)),
                ('address', models.TextField(default=None, max_length=300)),
                ('pincode', models.IntegerField(default=None)),
            ],
            options={
                'db_table': 'College Information',
            },
        ),
    ]
