# Generated by Django 4.2.3 on 2024-01-19 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_alter_event_eventid_alter_profile_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='eventId',
            field=models.CharField(default='', max_length=10, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(max_length=254, primary_key=True, serialize=False),
        ),
    ]
