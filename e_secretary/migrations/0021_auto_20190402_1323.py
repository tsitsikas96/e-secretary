# Generated by Django 2.1.7 on 2019-04-02 10:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_secretary', '0020_auto_20190402_1322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orologio',
            name='time',
        ),
        migrations.AddField(
            model_name='orologio',
            name='end_time',
            field=models.TimeField(default=datetime.datetime(2019, 4, 2, 13, 23, 45, 928069)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orologio',
            name='start_time',
            field=models.TimeField(default=datetime.datetime(2019, 4, 2, 13, 23, 52, 350053)),
            preserve_default=False,
        ),
    ]