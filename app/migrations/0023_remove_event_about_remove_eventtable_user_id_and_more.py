# Generated by Django 5.0 on 2023-12-20 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_remove_profile_joinyear_alter_profile_gradyear'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='about',
        ),
        migrations.RemoveField(
            model_name='eventtable',
            name='user_id',
        ),
        migrations.AddField(
            model_name='event',
            name='fee',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='eventtable',
            name='emails',
            field=models.TextField(default=''),
        ),
    ]