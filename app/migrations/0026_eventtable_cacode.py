# Generated by Django 4.2.3 on 2024-01-05 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_alter_event_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventtable',
            name='CACode',
            field=models.CharField(max_length=10, null=True),
        ),
    ]