# Generated by Django 2.0.5 on 2018-05-19 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='bio',
        ),
    ]