# Generated by Django 5.0 on 2024-01-09 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.EmailField(max_length=254)),
                ('address', models.TextField()),
                ('pincode', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('name', models.TextField()),
                ('itemId', models.CharField(default='', max_length=10, primary_key=True, serialize=False)),
                ('price', models.IntegerField(default=0)),
                ('size', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='PaymentTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transactionId', models.TextField()),
                ('itemId', models.CharField(max_length=10, null=True)),
                ('userId', models.EmailField(max_length=254)),
            ],
        ),
    ]