# Generated by Django 2.1.7 on 2019-04-02 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('e_secretary', '0027_simmetoxidrastiriotita_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='drastiriotita',
            old_name='didaskalia_id',
            new_name='didaskalia',
        ),
    ]