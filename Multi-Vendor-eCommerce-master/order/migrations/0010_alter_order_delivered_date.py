# Generated by Django 3.2.12 on 2023-06-20 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_auto_20211103_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivered_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]