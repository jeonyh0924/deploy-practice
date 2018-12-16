# Generated by Django 2.1.2 on 2018-12-16 03:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('containers', '0001_initial'),
        ('mappings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='webtrailercontainer',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mappings.Movie', verbose_name='영화'),
        ),
        migrations.AddField(
            model_name='apptrailercontainer',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mappings.Movie', verbose_name='영화'),
        ),
    ]
