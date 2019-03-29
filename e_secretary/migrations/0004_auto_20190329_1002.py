# Generated by Django 2.1.7 on 2019-03-29 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_secretary', '0003_auto_20190328_2124'),
    ]

    operations = [
        migrations.CreateModel(
            name='Secr_Announcement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField(help_text='Announcement to make')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['-date']},
        ),
    ]
