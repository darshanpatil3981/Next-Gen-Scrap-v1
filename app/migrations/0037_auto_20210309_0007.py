# Generated by Django 3.0.4 on 2021-03-08 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_auto_20210308_2253'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product_order',
            old_name='RC',
            new_name='RC_ID',
        ),
    ]
