# Generated by Django 3.2.12 on 2023-06-08 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0008_alter_customer_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='image',
            field=models.ImageField(blank=True, default='', null=True, upload_to='customers/'),
        ),
    ]
