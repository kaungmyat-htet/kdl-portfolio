# Generated by Django 3.2.22 on 2023-10-08 00:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kdl_portfolio', '0002_studentcareerinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('project_url', models.URLField()),
                ('role', models.CharField(max_length=40)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kdl_portfolio.student')),
            ],
        ),
        migrations.DeleteModel(
            name='Certificate',
        ),
        migrations.AddField(
            model_name='studentcareerinfo',
            name='skills',
            field=models.JSONField(default={}),
        ),
    ]