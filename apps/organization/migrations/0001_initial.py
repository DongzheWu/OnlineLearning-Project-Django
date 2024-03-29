# Generated by Django 2.2.6 on 2019-10-19 21:41

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CityDict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='City')),
                ('desc', models.CharField(max_length=200, verbose_name='CityDesc')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': 'Cities',
            },
        ),
        migrations.CreateModel(
            name='CourseOrg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='OrgName')),
                ('desc', models.TextField(verbose_name='OrgDesc')),
                ('click_nums', models.IntegerField(default=0, verbose_name='ClickNum')),
                ('fav_nums', models.IntegerField(default=0, verbose_name='fav_nums')),
                ('image', models.ImageField(upload_to='org/%Y/%m', verbose_name='Image')),
                ('address', models.CharField(max_length=150, verbose_name='OrgAddress')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.CityDict', verbose_name='City')),
            ],
            options={
                'verbose_name': 'Org',
                'verbose_name_plural': 'Orgs',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='TeacherName')),
                ('work_years', models.IntegerField(default=0, verbose_name='WorkYear')),
                ('work_company', models.CharField(max_length=50, verbose_name='Company')),
                ('work_position', models.CharField(max_length=50, verbose_name='Position')),
                ('points', models.CharField(max_length=50, verbose_name='points')),
                ('fav_nums', models.IntegerField(default=0, verbose_name='fav_nums')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.CourseOrg', verbose_name='OrgName')),
            ],
            options={
                'verbose_name': 'Teacher',
                'verbose_name_plural': 'Teachers',
            },
        ),
    ]
