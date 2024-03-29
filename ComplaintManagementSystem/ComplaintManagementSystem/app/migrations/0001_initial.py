# Generated by Django 3.2.18 on 2023-04-25 09:38

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Public_Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=30)),
                ('phone_number', models.CharField(max_length=30)),
                ('country', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=200)),
                ('username', models.CharField(max_length=200, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('image', models.FileField(null=True, upload_to='documents/', verbose_name='Upload Image')),
            ],
        ),
        migrations.CreateModel(
            name='Service_Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Rise_Complaint',
            fields=[
                ('reference_id', models.IntegerField(primary_key=True, serialize=False)),
                ('area', models.CharField(max_length=300)),
                ('address', models.TextField(max_length=2000)),
                ('msg', models.TextField(max_length=2000)),
                ('date', models.DateField(default=datetime.datetime(2023, 4, 25, 9, 38, 59, 99377, tzinfo=utc), null=True)),
                ('video', models.FileField(null=True, upload_to='video/', verbose_name='Upload Image/Video')),
                ('status', models.CharField(max_length=300)),
                ('initial_status', models.CharField(max_length=300)),
                ('public_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.public_detail')),
                ('service_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.service_detail')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=30)),
                ('date', models.DateField(default=datetime.datetime(2023, 4, 25, 9, 38, 59, 99377, tzinfo=utc), verbose_name='Posted Date')),
                ('query_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.rise_complaint')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.public_detail')),
            ],
        ),
    ]
