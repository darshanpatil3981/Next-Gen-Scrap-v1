# Generated by Django 2.0 on 2021-01-26 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210125_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gc',
            name='Profile_Pic',
            field=models.ImageField(default='d.jpg', upload_to='Profile_Pics'),
        ),
    ]