# Generated by Django 5.1.4 on 2025-07-18 20:09

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
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_id', models.CharField(max_length=100)),
                ('drug_name', models.CharField(max_length=100)),
                ('drug_category', models.CharField(default='unknown', max_length=100)),
                ('description', models.TextField(max_length=100)),
                ('quantity', models.IntegerField(default=0)),
                ('quantity_left', models.IntegerField(blank=True, null=True)),
                ('manufacture_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('batch_qr_code', models.ImageField(blank=True, null=True, upload_to='qr_codes/')),
                ('batch_qr_code_string', models.CharField(max_length=255, unique=True)),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parent_batch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sub_batches', to='manufacturer.batch')),
            ],
        ),
        migrations.CreateModel(
            name='BatchDistribution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_sent', models.IntegerField()),
                ('distribution_date', models.DateField(auto_now_add=True)),
                ('verified', models.BooleanField(default=False)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manufacturer.batch')),
                ('distributor', models.ForeignKey(limit_choices_to={'role': 'distributor'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to='qr_codes/')),
                ('qr_code_string', models.CharField(max_length=255, unique=True)),
                ('scanned', models.BooleanField(default=False)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manufacturer.batch')),
            ],
        ),
    ]
