# Generated by Django 2.1.7 on 2019-03-28 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField(help_text='Announcement to make')),
            ],
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('cert_id', models.AutoField(primary_key=True, serialize=False)),
                ('cert_type', models.CharField(max_length=50)),
                ('date_requested', models.DateField(auto_now_add=True)),
                ('available', models.BooleanField()),
                ('received', models.BooleanField()),
            ],
            options={
                'ordering': ['-cert_id'],
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Course Name', max_length=200)),
                ('tomeas', models.CharField(help_text='Tomeas Name', max_length=100)),
                ('ects', models.IntegerField()),
                ('programma_spoudwn', models.CharField(help_text='Programma Spoudwn', max_length=200)),
                ('ipoxrewtiko', models.BooleanField()),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Didaskalia',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('akad_etos', models.IntegerField(choices=[('EARINO', 'EARINO'), ('XEIMERINO', 'XEIMERINO')], default=2019)),
                ('eksamino', models.CharField(choices=[(1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019)], max_length=9)),
                ('course_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='e_secretary.Course')),
            ],
            options={
                'ordering': ['akad_etos'],
            },
        ),
        migrations.CreateModel(
            name='Dilosi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telikos_vathmos', models.FloatField(max_length=5)),
                ('didaskalies', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_secretary.Didaskalia')),
            ],
        ),
        migrations.CreateModel(
            name='Drastiriotita',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sintelestis', models.FloatField()),
                ('date', models.DateTimeField()),
                ('tipos', models.CharField(max_length=45)),
                ('didaskalia_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='e_secretary.Didaskalia')),
            ],
        ),
        migrations.CreateModel(
            name='Grammateia',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fname', models.CharField(help_text='First Name', max_length=50)),
                ('lname', models.CharField(help_text='Last Name', max_length=50)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Orologio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('day', models.CharField(choices=[('MON', 'MONDAY'), ('TUE', 'TUESDAY'), ('WEN', 'WENSDAY'), ('THU', 'THURSDAY'), ('FRI', 'FRIDAY'), ('SAT', 'SATURDAY'), ('SUN', 'SUNDAY')], max_length=3)),
                ('time', models.TimeField()),
                ('didaskalia_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='e_secretary.Didaskalia')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fname', models.CharField(max_length=20)),
                ('lname', models.CharField(max_length=20)),
                ('title', models.CharField(choices=[('PROF', 'Καθηγητής'), ('EPIK', 'Eπίκουρος Καθηγητής'), ('ANAPL', 'Αναπληρωτής Καθηγητής'), ('OMOT', 'Ομότιμος Καθηγητής'), ('EPIT', 'Επίτιμος Καθηγητής')], default='PROF', max_length=5)),
                ('email', models.EmailField(max_length=254)),
                ('tomeas', models.CharField(max_length=100)),
                ('didaskalia', models.ManyToManyField(to='e_secretary.Didaskalia')),
            ],
            options={
                'ordering': ['lname'],
            },
        ),
        migrations.CreateModel(
            name='SimmetoxiDrastiriotita',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('grade', models.FloatField(blank=True, null=True)),
                ('drastiriotita', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='e_secretary.Drastiriotita')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('am', models.AutoField(primary_key=True, serialize=False)),
                ('fname', models.CharField(max_length=20)),
                ('lname', models.CharField(max_length=20)),
                ('fathername', models.CharField(max_length=20)),
                ('age', models.IntegerField()),
                ('date_eisagwghs', models.DateField(auto_now_add=True)),
                ('department', models.CharField(max_length=100)),
                ('programma_spoudwn', models.CharField(max_length=10)),
                ('tomeas', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('didaskalia', models.ManyToManyField(through='e_secretary.Dilosi', to='e_secretary.Didaskalia')),
                ('drastiriotita', models.ManyToManyField(through='e_secretary.SimmetoxiDrastiriotita', to='e_secretary.Drastiriotita')),
            ],
            options={
                'ordering': ['-am'],
            },
        ),
        migrations.CreateModel(
            name='Thesis',
            fields=[
                ('thesis_id', models.AutoField(primary_key=True, serialize=False)),
                ('subject', models.TextField()),
                ('grade', models.FloatField(blank=True, null=True)),
                ('date_anathesis', models.DateField(auto_now_add=True)),
                ('date_paradosis', models.DateField(null=True)),
                ('student_am', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_secretary.Student')),
            ],
            options={
                'ordering': ['-thesis_id'],
            },
        ),
        migrations.AddField(
            model_name='simmetoxidrastiriotita',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='e_secretary.Student'),
        ),
        migrations.AddField(
            model_name='dilosi',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_secretary.Student'),
        ),
        migrations.AddField(
            model_name='certificate',
            name='student_am',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_secretary.Student'),
        ),
        migrations.AddField(
            model_name='announcement',
            name='didaskalia_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='e_secretary.Didaskalia'),
        ),
    ]