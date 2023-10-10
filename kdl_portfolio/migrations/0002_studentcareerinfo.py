# Generated by Django 3.2.22 on 2023-10-07 05:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kdl_portfolio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentCareerInfo',
            fields=[
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='kdl_portfolio.student')),
                ('profession', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('highest_level_degree', models.TextField()),
                ('institution', models.CharField(max_length=140)),
                ('phone_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
            ],
        ),
    ]
