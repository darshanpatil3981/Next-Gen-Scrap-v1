# Generated by Django 2.0 on 2020-12-16 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Firstname', models.CharField(max_length=30)),
                ('Lastname', models.CharField(max_length=30)),
                ('Address', models.CharField(max_length=100)),
                ('City', models.CharField(max_length=30)),
                ('State', models.CharField(max_length=30)),
                ('Pincode', models.BigIntegerField()),
                ('Contact', models.BigIntegerField(default=0)),
                ('Profile_Pic', models.ImageField(upload_to='app/Profile_Pics')),
            ],
        ),
        migrations.CreateModel(
            name='GC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Firstname', models.CharField(max_length=30)),
                ('Lastname', models.CharField(max_length=30)),
                ('Address', models.CharField(max_length=100)),
                ('City', models.CharField(max_length=30)),
                ('State', models.CharField(max_length=30)),
                ('Pincode', models.BigIntegerField()),
                ('Contact', models.BigIntegerField(default=0)),
                ('Profile_Pic', models.ImageField(upload_to='app/Profile_Pics')),
            ],
        ),
        migrations.CreateModel(
            name='RC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Firstname', models.CharField(max_length=30)),
                ('Lastname', models.CharField(max_length=30)),
                ('Address', models.CharField(max_length=100)),
                ('City', models.CharField(max_length=30)),
                ('State', models.CharField(max_length=30)),
                ('Pincode', models.BigIntegerField()),
                ('Contact', models.BigIntegerField(default=0)),
                ('Profile_Pic', models.ImageField(upload_to='app/Profile_Pics')),
            ],
        ),
        migrations.CreateModel(
            name='User_Master',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Email', models.EmailField(max_length=50)),
                ('Password', models.CharField(max_length=50)),
                ('Role', models.CharField(max_length=20)),
                ('Otp', models.IntegerField()),
                ('is_created', models.DateTimeField(auto_now=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='rc',
            name='RC_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.User_Master'),
        ),
        migrations.AddField(
            model_name='gc',
            name='GC_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.User_Master'),
        ),
        migrations.AddField(
            model_name='customer',
            name='Customer_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.User_Master'),
        ),
    ]