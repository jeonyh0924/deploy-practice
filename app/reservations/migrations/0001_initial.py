# Generated by Django 2.1.2 on 2018-11-29 06:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Auditorium',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('seats_no', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(error_messages={'unique': 'The Movie with that title already exists.'}, max_length=50, unique=True)),
                ('director', models.CharField(max_length=30)),
                ('cast', models.CharField(max_length=150)),
                ('duration_min', models.IntegerField()),
                ('opening_date', models.DateField()),
                ('genre', models.CharField(max_length=20)),
                ('description', models.TextField(max_length=200)),
                ('trailer', models.URLField(blank=True, null=True)),
                ('stillcut', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Screening',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('screening_time', models.DateTimeField()),
                ('auditorium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.Auditorium')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.CharField(max_length=5)),
                ('number', models.IntegerField()),
                ('reservation_check', models.BooleanField()),
                ('auditorium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.Auditorium')),
            ],
        ),
        migrations.CreateModel(
            name='Theater',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=10)),
                ('sub_location', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=50)),
                ('current_movies', models.ManyToManyField(related_name='theater_set', related_query_name='theater', through='reservations.Screening', to='reservations.Movie')),
            ],
        ),
        migrations.AddField(
            model_name='screening',
            name='theater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.Theater'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='screening',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.Screening'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='seat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.Seat'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='auditorium',
            name='theater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.Theater'),
        ),
    ]
