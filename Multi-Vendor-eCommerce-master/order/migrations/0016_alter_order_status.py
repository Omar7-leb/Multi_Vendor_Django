# Generated by Django 3.2.12 on 2023-06-23 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0015_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered'), ('archived', 'Archived - not available anymore')], default='Processing', max_length=200, null=True),
        ),
    ]
