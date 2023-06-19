# Generated by Django 3.2.12 on 2023-06-17 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0009_alter_customer_image'),
        ('order', '0012_auto_20230618_0141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ManyToManyField(to='customers.Customer'),
        ),
    ]
