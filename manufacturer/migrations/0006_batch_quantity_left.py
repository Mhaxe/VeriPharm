# Generated by Django 5.1.4 on 2025-06-16 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturer', '0005_batch_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='quantity_left',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
