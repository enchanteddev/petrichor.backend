# Generated by Django 4.2.3 on 2023-08-18 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_profile_username_alter_profile_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='college',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='year',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
