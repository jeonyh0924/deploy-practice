import re

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.db.models import Q

User = get_user_model()


# Create your models here.
# Movie - Screening - Theater를 연결한다.
# Screening은 Movie와 Theater의 intermediate개체


# Dynamic Path for Media File upload_to
def movie_directory_path(instance, filename):
    directory = instance.title
    return f'{directory}/{filename}'


def still_cut_directory_path(instance, filename):
    directory = instance.movie.title
    return f'{directory}/{filename}'


def director_directory_path(instance, filename):
    directory = instance.director
    return f'{directory}/{filename}'


def cast_directory_path(instance, filename):
    directory = instance.actor
    return f'{directory}/{filename}'


# 영화(Movie) 객체 모델
class Movie(models.Model):

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '영화'
        verbose_name_plural = f'{verbose_name} 목록'
        # 예매율 순위로 리스트 순서 변경
        ordering = ['reservation_score']

    # 타이틀
    title = models.CharField(max_length=50, blank=True, null=True, verbose_name='타이틀')
    # 타이틀(영어)
    eng_title = models.CharField(max_length=50, blank=True, null=True, verbose_name='타이틀(영문)')
    # 러닝타임
    duration_min = models.PositiveIntegerField(blank=True, null=True, verbose_name='러닝타임')
    # 연령 제한
    age = models.CharField(max_length=32, blank=True, null=True, verbose_name='연령 제한')
    # 개봉일
    opening_date = models.DateField(blank=True, null=True, verbose_name='개봉일')
    # 영화 장르
    genre = models.CharField(max_length=32, blank=True, null=True, verbose_name='장르')
    # 영화 줄거리
    description = models.TextField(max_length=512, blank=True, null=True, verbose_name='줄거리')
    # 트레일러
    trailer = models.URLField(default='', blank=True, null=True, verbose_name='트레일러')
    # 예매율
    reservation_score = models.FloatField(default=0, blank=True, null=True, verbose_name='예매율')
    # 개봉 여부
    now_open = models.BooleanField(default=False, blank=True, null=True, verbose_name='개봉 여부')
    # 상영 여부
    now_show = models.BooleanField(default=False, blank=True, null=True, verbose_name='상영 여부')
    # 영화 메인 포스터
    main_img = models.ImageField(upload_to=movie_directory_path, blank=True, null=True, verbose_name='메인 포스터')


# 감독
class Director(models.Model):
    def __str__(self):
        return self.director

    class Meta:
        verbose_name = '감독'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['pk']

    movie = models.ManyToManyField(Movie, through='Directing', related_name='directors', related_query_name='director', blank=True, verbose_name='영화')
    director = models.CharField(max_length=64, blank=True, null=True, verbose_name='감독')
    eng_director = models.CharField(max_length=64, blank=True, null=True, verbose_name='감독(영문)')
    profile_img = models.ImageField(upload_to=director_directory_path, blank=True, null=True, verbose_name='감독 프로필 사진')


# 디렉팅
class Directing(models.Model):
    movie = models.ForeignKey(Movie, null=True, blank=True, on_delete=models.CASCADE)
    director = models.ForeignKey(Director, null=True, blank=True, on_delete=models.CASCADE)


# 출연배우
class Cast(models.Model):
    def __str__(self):
        return self.actor

    class Meta:
        verbose_name = '배우'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['pk']
    movie = models.ManyToManyField(Movie, through='Casting', related_name='casts', related_query_name='cast', blank=True, verbose_name='영화')
    actor = models.CharField(max_length=64, blank=True, null=True, verbose_name='배우')
    eng_actor = models.CharField(max_length=64, blank=True, null=True, verbose_name='배우(영문)')
    profile_img = models.ImageField(upload_to=cast_directory_path, blank=True, null=True, verbose_name='배우 프로필 사진')


CASTING_CHOICE = (
    ('주연', 'Main'),
    ('조연', 'Sub'),
)

# 캐스팅(주/조연)
class Casting(models.Model):
    movie = models.ForeignKey(Movie, null=True, blank=True, on_delete=models.CASCADE)
    actor = models.ForeignKey(Cast, null=True, blank=True, on_delete=models.CASCADE)
    cast = models.CharField(max_length=32, choices=CASTING_CHOICE, null=True, blank=True)


# 스틸컷
class Stillcut(models.Model):
    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = '스틸컷'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['pk']

    movie = models.ForeignKey(Movie, related_name='stillcuts', on_delete=models.CASCADE, verbose_name='영화')
    image = models.ImageField(upload_to=still_cut_directory_path, verbose_name='스틸컷 이미지')


# 영화관(Theater) 객체 모델
class Theater(models.Model):
    def __str__(self):
        return self.sub_location

    class Meta:
        verbose_name = '극장'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['pk']

    # 지역 대분류(광역시/도 단위 카테고리 ex) 서울 / 충청남도)
    location = models.CharField(max_length=10, verbose_name='지역')
    # 지역 소분류 = 영화관 이름( ex)강남점, 신촌점)
    sub_location = models.CharField(max_length=15, verbose_name='지점')
    # 세부 주소정보 : 텍스트 주소 or 경도/위도 사용
    address = models.CharField(max_length=50, verbose_name='주소')

    # 상영중인 영화(Movie 목록)
    current_movies = models.ManyToManyField(
        Movie,
        through='Screening',
        related_name='theaters',
        related_query_name='theater',
        verbose_name='상영 영화',
        blank=True,
    )


# 상영관(Auditorium) 객체 모델
class Auditorium(models.Model):
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '상영관'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['pk']

    # 상영관 이름( ex) A관, 2관 .... )
    name = models.CharField(max_length=10, verbose_name='상영관 이름')
    # 좌석수
    seats_no = models.PositiveIntegerField(default=0, verbose_name='좌석 수')
    # 소속 영화관
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, verbose_name='소속 영화관', related_name='auditoriums')


# 좌석(Seat) 객체 모델
class Seat(models.Model):
    def __str__(self):
        return f'{self.row}행 {self.number}열'

    class Meta:
        verbose_name = '좌석'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['pk']

    # 좌석 위치(행)
    row = models.PositiveIntegerField(verbose_name='행')
    # 좌석 위치(열)
    number = models.PositiveIntegerField(verbose_name='열')
    # 배치 상영관
    auditorium = models.ForeignKey(Auditorium, on_delete=models.CASCADE, verbose_name='배치 상영관', related_name='seats')
    # Seat Name
    seat_name = models.CharField(max_length=4)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Seat, self).save()
        self.auditorium.seats_no = len(Seat.objects.filter(auditorium=self.auditorium))
        self.auditorium.save()

    def delete(self, using=None, keep_parents=False):
        super(Seat, self).delete()
        self.auditorium.seats_no = len(Seat.objects.filter(auditorium=self.auditorium))
        self.auditorium.save()


# 상영(Screening) 객체 모델
class Screening(models.Model):
    def __str__(self):
        return self.movie.title

    class Meta:
        verbose_name = '상영'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['pk']

    # 상영 영화
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='상영 영화', related_name='screenings')
    # 상영 영화관(theater)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, verbose_name='상영 영화관', related_name='screenings')
    # 상영관(auditorium)
    auditorium = models.ForeignKey(Auditorium, on_delete=models.CASCADE, verbose_name='상영관', related_name='screenings')
    # 상영 시간
    time = models.DateTimeField(verbose_name='상영 시간')
    # 각 상영시간 단위 Seat
    reserved_seats = models.ManyToManyField(
        Seat,
        through='ReservedSeat',
        related_name='screens',
        related_query_name='screen',
    )


# 예매된 좌석. 선택한 좌석의 pk가 전달되면 해당 좌석을 참조하고, 앞서 선택한 상영시간을 참조하는 예매 좌석 객체를 생성한다.
# 생성된 예매 좌석 객체를 참조하여 Reservation 객체가 생성된다.
class ReservedSeat(models.Model):
    def __str__(self):
        return self.seat

    class Meta:
        verbose_name = '예약 좌석'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['pk']

    screening = models.ForeignKey(Screening, on_delete=models.CASCADE, related_name='selected_seats', verbose_name='상영시간')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, verbose_name='좌석')


# 예매(Reservation) 객체 모델
class Reservation(models.Model):
    def __str__(self):
        return f'{self.user} / {self.screening}'

    class Meta:
        verbose_name = '예약'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['pk']

    # 예매 유저
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='예매자', related_name='reservations', related_query_name='reservation')
    # 예매 상영 정보(상영관), 상영 시간
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE, blank=True, null=True, verbose_name='상영 예매')
    # 예매 상영 시간
    # screening_time = models.ForeignKey(ScreeningTime, on_delete=models.CASCADE, blank=True, null=True, verbose_name='예매 시간')
    # 예매 좌석 정보
    seat = models.ForeignKey(ReservedSeat, on_delete=models.CASCADE)
    # 결제 완료 시점(예매 시간)
    # created_at = models.DateTimeField(auto_now_add=True)
    # 취소 여부 확인
    is_active = models.BooleanField(default=True, verbose_name='활성화')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Reservation, self).save()
        # 예매 취소(is_active = False) 전환 시에도 아래 예매율 변동 처리를 넣을 것.
        Instance = self.screening.movie
        active_reservations = Reservation.objects.filter(is_active=True)
        Instance.reservation_score = len(active_reservations.objects.filter(movie=Instance)) / len(active_reservations)
        Instance.save()


# 이후 reservation_type (ex) 청소년, 일반 ...)을 추가할 수 있다.
# 이 경우는 Reservation에 reservation_type 필드를 추가하고,
# class Reservation_Type(models.Model)을 추가한다.
# Charfield + Choice_Set을 구성한다.(or CHOICE FIELD를 사용)
