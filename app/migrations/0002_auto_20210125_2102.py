# Generated by Django 2.0 on 2021-01-25 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='Profile_Pic',
            field=models.ImageField(default='d.jpg', upload_to='app/Profile_Pics'),
        ),
        migrations.AlterField(
            model_name='gc',
            name='Profile_Pic',
            field=models.ImageField(default='d.jpg', upload_to='app/Profile_Pics'),
        ),
        migrations.AlterField(
            model_name='rc',
            name='Profile_Pic',
            field=models.ImageField(default='d.jpg', upload_to='app/Profile_Pics'),
        ),
    ]