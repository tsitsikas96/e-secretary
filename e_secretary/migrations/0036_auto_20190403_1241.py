# Generated by Django 2.1.7 on 2019-04-03 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_secretary', '0035_auto_20190403_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='programma_spoudwn',
            field=models.CharField(choices=[('HMTY_Bachelor', 'HMTY_Bachelor'), ('HMTY_Masters', 'HMTY_Masters')], help_text='Programma Spoudwn', max_length=45),
        ),
    ]