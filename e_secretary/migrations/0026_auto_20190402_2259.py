# Generated by Django 2.1.7 on 2019-04-02 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_secretary', '0025_auto_20190402_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drastiriotita',
            name='tipos',
            field=models.CharField(choices=[('ERGASIA', 'ERGASIA'), ('PROODOS', 'PROODOS'), ('ERGASTIRIO', 'ERGASTIRIO'), ('EKSTETASTIKI', 'EKSTETASTIKI')], max_length=25),
        ),
    ]
