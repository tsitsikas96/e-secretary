# Generated by Django 2.1.7 on 2019-04-03 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_secretary', '0029_simmetoxidrastiriotita_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='simmetoxidrastiriotita',
            name='title',
        ),
        migrations.AddField(
            model_name='drastiriotita',
            name='title',
            field=models.CharField(default='Test', max_length=45),
            preserve_default=False,
        ),
    ]
