# Generated by Django 4.1.7 on 2023-05-03 10:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_staff_detail_alter_feedback_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 5, 3, 10, 23, 53, 659282, tzinfo=datetime.timezone.utc), verbose_name='Posted Date'),
        ),
        migrations.AlterField(
            model_name='rise_complaint',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 5, 3, 10, 23, 53, 659282, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
