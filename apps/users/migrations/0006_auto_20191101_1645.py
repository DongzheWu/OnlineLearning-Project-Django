# Generated by Django 2.2.6 on 2019-11-01 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20191020_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_type',
            field=models.CharField(choices=[('r', 'register'), ('f', 'forgot'), ('update_email', 'modify')], max_length=30, verbose_name='SendType'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('femaile', 'female')], default='femaile', max_length=10),
        ),
    ]
