# Generated by Django 3.0.4 on 2021-02-24 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_product_order_payment_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product_order',
            name='Customer_ID',
        ),
    ]