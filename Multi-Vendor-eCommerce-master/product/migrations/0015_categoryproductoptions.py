# Generated by Django 3.2.12 on 2023-06-13 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_remove_product_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryProductOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField(max_length=30)),
                ('category_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.categoryoptions')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]