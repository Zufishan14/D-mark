# Generated by Django 5.1.6 on 2025-03-05 08:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0004_person_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True, validators=[django.core.validators.EmailValidator]),
        ),
    ]
