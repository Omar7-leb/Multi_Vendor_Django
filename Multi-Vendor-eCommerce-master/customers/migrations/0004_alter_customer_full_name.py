# Generated by Django 3.2.6 on 2021-09-16 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_alter_customer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='full_name',
            field=models.CharField(max_length=255),
        ),
    ]
