# Generated by Django 2.2.6 on 2019-10-26 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='category',
            field=models.CharField(choices=[('pxjg', 'pxjg'), ('gr', 'gr'), ('gx', 'gx')], default='pxjg', max_length=20, verbose_name='category'),
        ),
    ]