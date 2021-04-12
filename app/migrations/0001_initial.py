# Generated by Django 2.0 on 2021-04-12 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User_Name', models.EmailField(max_length=50)),
                ('Password', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Areas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cust_Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Quantity', models.IntegerField(default=0)),
                ('Total_Amount', models.IntegerField(default=0)),
            ],
        ),
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
                ('Profile_Pic', models.ImageField(default='user.png', upload_to='Profile_Pics')),
            ],
        ),
        migrations.CreateModel(
            name='Customer_Scrap_Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, max_length=50, null=True)),
                ('Phone', models.BigIntegerField()),
                ('Email', models.EmailField(max_length=254)),
                ('Address', models.CharField(blank=True, max_length=200, null=True)),
                ('Pincode', models.IntegerField()),
                ('City', models.CharField(blank=True, max_length=20, null=True)),
                ('State', models.CharField(blank=True, max_length=20, null=True)),
                ('Datetime_Of_Pickup', models.DateTimeField()),
                ('Is_Complited', models.BooleanField(default=False)),
                ('Customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Ecom_comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Comment_text', models.CharField(max_length=500)),
                ('Comment_time', models.DateTimeField()),
                ('Customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Order_id', models.CharField(blank=True, default=None, max_length=100, null=True, unique=True)),
                ('Total_Amount', models.FloatField(default=0)),
                ('Sub_Total_Amount', models.FloatField(default=0)),
                ('Payment_status', models.CharField(blank=True, max_length=20, null=True)),
                ('Datetime_of_payment', models.DateField(null=True)),
                ('Invoice_No', models.BigIntegerField(default=0)),
                ('Razorpay_order_id', models.CharField(blank=True, max_length=500, null=True)),
                ('Razorpay_payment_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_signature', models.CharField(blank=True, max_length=500, null=True)),
                ('Customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Seller_Name', models.CharField(default='', max_length=30)),
                ('Product_Name', models.CharField(max_length=30)),
                ('Product_Price', models.FloatField()),
                ('Product_Desc', models.TextField()),
                ('Product_Img', models.ImageField(default='', upload_to='Product_Images')),
                ('Current_orders', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Product_Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RC_ID', models.CharField(blank=True, max_length=20, null=True)),
                ('Customer', models.CharField(blank=True, max_length=20, null=True)),
                ('Cart_ID', models.CharField(blank=True, max_length=20, null=True)),
                ('Payment_status', models.CharField(blank=True, max_length=20, null=True)),
                ('Quantity', models.PositiveIntegerField()),
                ('Price', models.FloatField(default=0)),
                ('Order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Order')),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Product')),
            ],
        ),
        migrations.CreateModel(
            name='RC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Firstname', models.CharField(max_length=30)),
                ('Lastname', models.CharField(max_length=30)),
                ('Company_name', models.CharField(default='', max_length=30)),
                ('Address', models.CharField(max_length=100)),
                ('City', models.CharField(max_length=30)),
                ('State', models.CharField(max_length=30)),
                ('Pincode', models.BigIntegerField()),
                ('Contact', models.BigIntegerField(default=0)),
                ('Profile_Pic', models.ImageField(default='user.png', upload_to='Profile_Pics')),
            ],
        ),
        migrations.CreateModel(
            name='RC_Scrap_Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Quantity', models.IntegerField(null=True)),
                ('Datetime_of_request', models.DateTimeField()),
                ('Is_Complited', models.BooleanField(default=False)),
                ('RC', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.RC')),
            ],
        ),
        migrations.CreateModel(
            name='SC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Firstname', models.CharField(max_length=30)),
                ('Lastname', models.CharField(max_length=30)),
                ('Shop_name', models.CharField(default='', max_length=30)),
                ('Address', models.CharField(max_length=100)),
                ('City', models.CharField(max_length=30)),
                ('Area', models.CharField(blank=True, max_length=30, null=True)),
                ('State', models.CharField(max_length=30)),
                ('Pincode', models.BigIntegerField()),
                ('Contact', models.BigIntegerField(default=0)),
                ('Profile_Pic', models.ImageField(default='user.png', upload_to='Profile_Pics')),
            ],
        ),
        migrations.CreateModel(
            name='Scrap_Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, max_length=20, null=True)),
                ('Price', models.FloatField()),
                ('Image', models.ImageField(default='default.png', upload_to='Scrap_Images')),
            ],
        ),
        migrations.CreateModel(
            name='Scrap_Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Quantity', models.IntegerField(null=True)),
                ('Name', models.CharField(blank=True, max_length=20, null=True)),
                ('Price', models.FloatField()),
                ('Image', models.ImageField(default='default.png', upload_to='Scrap_Images')),
                ('In_Stock', models.BooleanField()),
                ('SC', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.SC')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Role', models.CharField(blank=True, max_length=10, null=True)),
                ('Is_Active', models.BooleanField()),
                ('Subscription_Name', models.CharField(blank=True, max_length=20, null=True)),
                ('Subscription_Amount', models.FloatField(default=0)),
                ('Subscription_Starting_Date', models.DateField()),
                ('Subscription_Ending_Date', models.DateField()),
                ('Invoice_No', models.BigIntegerField(default=0)),
                ('Razorpay_order_id', models.CharField(blank=True, max_length=500, null=True)),
                ('Razorpay_payment_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_signature', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User_Master',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Email', models.EmailField(max_length=50)),
                ('Password', models.CharField(max_length=300)),
                ('Role', models.CharField(max_length=20)),
                ('is_created', models.DateTimeField(auto_now=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_updated', models.DateTimeField(auto_now=True)),
                ('Verify_Request', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='subscription',
            name='User',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.User_Master'),
        ),
        migrations.AddField(
            model_name='sc',
            name='User_Master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.User_Master'),
        ),
        migrations.AddField(
            model_name='rc_scrap_request',
            name='SC',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.SC'),
        ),
        migrations.AddField(
            model_name='rc_scrap_request',
            name='Scrap_Stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Scrap_Stock'),
        ),
        migrations.AddField(
            model_name='rc',
            name='User_Master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.User_Master'),
        ),
        migrations.AddField(
            model_name='product',
            name='RC',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.RC'),
        ),
        migrations.AddField(
            model_name='ecom_comments',
            name='Product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Product'),
        ),
        migrations.AddField(
            model_name='customer_scrap_request',
            name='SC',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.SC'),
        ),
        migrations.AddField(
            model_name='customer',
            name='User_Master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.User_Master'),
        ),
        migrations.AddField(
            model_name='cust_cart',
            name='Customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Customer'),
        ),
        migrations.AddField(
            model_name='cust_cart',
            name='Product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Product'),
        ),
    ]
