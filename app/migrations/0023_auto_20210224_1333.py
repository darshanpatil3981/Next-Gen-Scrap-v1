# Generated by Django 3.0.4 on 2021-02-24 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_order_razorpay_signature'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_order',
            name='Customer_ID',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='product_order',
            name='RC_ID',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]