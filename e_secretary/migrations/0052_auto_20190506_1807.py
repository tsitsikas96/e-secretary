# Generated by Django 2.2 on 2019-05-06 15:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_secretary', '0051_auto_20190506_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='date_requested',
            field=models.DateField(default=datetime.datetime(2019, 5, 6, 18, 7, 50, 530338)),
        ),
    ]