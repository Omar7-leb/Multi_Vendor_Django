# Generated by Django 3.2.12 on 2023-06-21 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_alter_order_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='isPaid',
            field=models.BooleanField(default=True),
        ),
    ]
