# Generated by Django 2.1.7 on 2019-04-02 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_secretary', '0022_auto_20190402_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dilosi',
            name='telikos_vathmos',
            field=models.FloatField(blank=True, max_length=4, null=True),
        ),
    ]