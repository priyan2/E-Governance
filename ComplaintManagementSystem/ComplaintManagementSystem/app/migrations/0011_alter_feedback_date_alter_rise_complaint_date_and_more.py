# Generated by Django 4.1.7 on 2023-05-09 04:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_feedback_date_alter_rise_complaint_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 5, 9, 4, 27, 6, 965835, tzinfo=datetime.timezone.utc), verbose_name='Posted Date'),
        ),
        migrations.AlterField(
            model_name='rise_complaint',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 5, 9, 4, 27, 6, 965835, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='rise_complaint',
            name='reference_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
