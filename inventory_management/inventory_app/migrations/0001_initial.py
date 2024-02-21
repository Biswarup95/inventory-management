# Generated by Django 5.0.2 on 2024-02-16 11:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(max_length=50)),
                ('product_name', models.CharField(max_length=100)),
                ('vendor', models.CharField(max_length=100)),
                ('mrp', models.DecimalField(decimal_places=2, max_digits=10)),
                ('batch_num', models.CharField(max_length=50)),
                ('batch_date', models.DateField()),
                ('quantity', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('Approved', 'Approved'), ('Pending', 'Pending')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('Department Manager', 'Department Manager'), ('Store Manager', 'Store Manager')], max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]