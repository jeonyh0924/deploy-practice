# Generated by Django 2.1.2 on 2018-12-17 11:48

from django.db import migrations, models
import django.db.models.deletion
import mappings.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auditorium',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='상영관 이름')),
                ('seats_no', models.PositiveIntegerField(default=0, verbose_name='좌석 수')),
            ],
            options={
                'verbose_name': '상영관',
                'verbose_name_plural': '상영관 목록',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Cast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actor', models.CharField(blank=True, max_length=64, null=True, verbose_name='배우')),
                ('eng_actor', models.CharField(blank=True, max_length=64, null=True, verbose_name='배우(영문)')),
                ('profile_img', models.ImageField(blank=True, null=True, upload_to=mappings.models.cast_directory_path, verbose_name='배우 프로필 사진')),
            ],
            options={
                'verbose_name': '배우',
                'verbose_name_plural': '배우 목록',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Casting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cast', models.CharField(blank=True, choices=[('주연', 'Main'), ('조연', 'Sub')], max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Directing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('director', models.CharField(blank=True, max_length=64, null=True, verbose_name='감독')),
                ('eng_director', models.CharField(blank=True, max_length=64, null=True, verbose_name='감독(영문)')),
                ('profile_img', models.ImageField(blank=True, null=True, upload_to=mappings.models.director_directory_path, verbose_name='감독 프로필 사진')),
            ],
            options={
                'verbose_name': '감독',
                'verbose_name_plural': '감독 목록',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50, null=True, verbose_name='타이틀')),
                ('eng_title', models.CharField(blank=True, max_length=50, null=True, verbose_name='타이틀(영문)')),
                ('duration_min', models.PositiveIntegerField(blank=True, null=True, verbose_name='러닝타임')),
                ('age', models.CharField(blank=True, max_length=32, null=True, verbose_name='연령 제한')),
                ('opening_date', models.DateField(blank=True, null=True, verbose_name='개봉일')),
                ('genre', models.CharField(blank=True, max_length=32, null=True, verbose_name='장르')),
                ('description', models.TextField(blank=True, max_length=1024, null=True, verbose_name='줄거리')),
                ('trailer', models.URLField(blank=True, default='', null=True, verbose_name='트레일러')),
                ('reservation_score', models.FloatField(blank=True, default=0, null=True, verbose_name='예매율')),
                ('now_open', models.BooleanField(blank=True, default=False, null=True, verbose_name='개봉 여부')),
                ('now_show', models.BooleanField(blank=True, default=False, null=True, verbose_name='상영 여부')),
                ('main_img', models.ImageField(blank=True, null=True, upload_to=mappings.models.movie_directory_path, verbose_name='메인 포스터')),
            ],
            options={
                'verbose_name': '영화',
                'verbose_name_plural': '영화 목록',
                'ordering': ['reservation_score'],
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='활성화')),
                ('get_paid', models.BooleanField(default=True, verbose_name='결제 여부')),
            ],
            options={
                'verbose_name': '예약',
                'verbose_name_plural': '예약 목록',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='ReservedSeat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats_reserved', to='mappings.Reservation', verbose_name='예매')),
            ],
            options={
                'verbose_name': '예약 좌석',
                'verbose_name_plural': '예약 좌석 목록',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Screening',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(verbose_name='상영 시간')),
                ('auditorium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='screenings', to='mappings.Auditorium', verbose_name='상영관')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='screenings', to='mappings.Movie', verbose_name='상영 영화')),
            ],
            options={
                'verbose_name': '상영',
                'verbose_name_plural': '상영 목록',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.PositiveIntegerField(verbose_name='행')),
                ('number', models.PositiveIntegerField(verbose_name='열')),
                ('seat_name', models.CharField(max_length=4)),
                ('auditorium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='mappings.Auditorium', verbose_name='배치 상영관')),
            ],
            options={
                'verbose_name': '좌석',
                'verbose_name_plural': '좌석 목록',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Stillcut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=mappings.models.still_cut_directory_path, verbose_name='스틸컷 이미지')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stillcuts', to='mappings.Movie', verbose_name='영화')),
            ],
            options={
                'verbose_name': '스틸컷',
                'verbose_name_plural': '스틸컷 목록',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Theater',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=10, verbose_name='지역')),
                ('sub_location', models.CharField(max_length=15, verbose_name='지점')),
                ('address', models.CharField(max_length=50, verbose_name='주소')),
                ('current_movies', models.ManyToManyField(blank=True, related_name='theaters', related_query_name='theater', through='mappings.Screening', to='mappings.Movie', verbose_name='상영 영화')),
            ],
            options={
                'verbose_name': '극장',
                'verbose_name_plural': '극장 목록',
                'ordering': ['pk'],
            },
        ),
        migrations.AddField(
            model_name='screening',
            name='reserved_seats',
            field=models.ManyToManyField(related_name='screens', related_query_name='screen', through='mappings.ReservedSeat', to='mappings.Seat'),
        ),
        migrations.AddField(
            model_name='screening',
            name='theater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='screenings', to='mappings.Theater', verbose_name='상영 영화관'),
        ),
        migrations.AddField(
            model_name='reservedseat',
            name='screening',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mappings.Screening', verbose_name='상영시간'),
        ),
        migrations.AddField(
            model_name='reservedseat',
            name='seat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mappings.Seat', verbose_name='좌석'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='screening',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mappings.Screening', verbose_name='상영 예매'),
        ),
    ]