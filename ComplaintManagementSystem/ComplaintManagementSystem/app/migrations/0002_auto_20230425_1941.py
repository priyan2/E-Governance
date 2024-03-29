# Generated by Django 3.2.18 on 2023-04-25 14:11

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category_Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.AlterField(
            model_name='feedback',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 4, 25, 14, 11, 9, 642373, tzinfo=utc), verbose_name='Posted Date'),
        ),
        migrations.AlterField(
            model_name='rise_complaint',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 4, 25, 14, 11, 9, 642373, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='rise_complaint',
            name='service_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.category_detail'),
        ),
        migrations.DeleteModel(
            name='Service_Detail',
        ),
    ]
