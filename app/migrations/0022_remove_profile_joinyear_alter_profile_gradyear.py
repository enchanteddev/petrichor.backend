# Generated by Django 4.2.3 on 2023-12-18 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_remove_event_id_remove_eventtable_ca_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='joinYear',
        ),
        migrations.AlterField(
            model_name='profile',
            name='gradYear',
            field=models.IntegerField(default=6969),
        ),
    ]
