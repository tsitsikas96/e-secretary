# Generated by Django 2.2 on 2019-05-02 19:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_secretary', '0041_auto_20190408_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dilosi',
            name='telikos_vathmos',
            field=models.FloatField(blank=True, max_length=4, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)]),
        ),
        migrations.AlterField(
            model_name='simmetoxidrastiriotita',
            name='grade',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)]),
        ),
    ]
