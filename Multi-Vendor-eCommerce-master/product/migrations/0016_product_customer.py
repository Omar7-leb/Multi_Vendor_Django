# Generated by Django 3.2.12 on 2023-06-20 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0009_alter_customer_image'),
        ('product', '0015_categoryproductoptions'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='customers.customer'),
        ),
    ]
