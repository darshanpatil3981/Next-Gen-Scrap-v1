# Generated by Django 2.0 on 2021-02-09 04:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20210207_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_master',
            name='Otp',
        ),
    ]
