# Generated by Django 3.0.2 on 2020-01-13 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0003_college_yearofestablishment'),
    ]

    operations = [
        migrations.AddField(
            model_name='college',
            name='image',
            field=models.ImageField(default='College/media/default.jpg', upload_to='College/media'),
        ),
    ]
