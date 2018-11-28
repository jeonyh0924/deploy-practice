from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()

# Create your models here.
# Movie - Screening - Theater를 연결한다.
# Screening은 Movie와 Theater의 intermediate개체


# 영화(Movie) 객체 모델
class Movie(models.Model):
    # 타이틀
    title = models.CharField(
        max_length=50, unique=True,
        error_messages={
            'unique': "The Movie with that title already exists.",
        },
    )
    # 감독
    director = models.CharField(max_length=30)

    # 출연배우(cast) 관련 수정 가능 사항
    # 만약 배우를 새로운 object로 만들어 해당 배우 정보 및 출연작 정보를
    # 나타내도록 구현하고자 한다면 cast = models.ManyToManyField로 만들어야한다.

    # List(Array) object를 저장할 수 있는 modelfield는 없는 것으로 보인다
    # 이 경우 두 가지의 방법을 생각할 수 있다
    # 1) 'obj1, obj2, ... ' 의 charfield로 받은 후, 이후 사용시 split() method로
    # list도 추후에 환원한다.
    # 2) PostgreSQL을 사용하는 경우, 이들 library에서 ArrayField를 import하는 방법이 있다.

    # 출연 배우
    cast = models.CharField(max_length=150)
    # 상영시간
    duration_min = models.IntegerField()
    # 개봉일
    opening_date = models.DateField()
    # 영화 장르
    genre = models.CharField(max_length=20)
    # 영화 줄거리
    description = models.TextField(max_length=200)
    # 트레일러
    trailer = models.URLField(blank=True, null=True)


# 영화관(Theater) 객체 모델
class Theater(models.Model):
    # 지역 대분류(광역시/도 단위 카테고리 ex) 서울 / 충청남도)
    location = models.CharField(max_length=10)
    # 지역 소분류 = 영화관 이름( ex)강남점, 신촌점)
    sub_location = models.CharField(max_length=15)
    # 세부 주소정보 : 텍스트 주소 or 경도/위도 사용
    address = models.CharField(max_length=50)

    # 상영중인 영화(Movie 목록)
    # 이후 immediate를 through로 설정히가나
    # related_name, related_query_name을 아래에 설정해야 한다.
    current_movies = models.ManyToManyField(
        Movie,
        through='Screening',
        related_name='theater_set',
        related_query_name='theater',
    )


# 상영관(Auditorium) 객체 모델
class Auditorium(models.Model):
    # 상영관 이름( ex) A관, 2관 .... )
    name = models.CharField(max_length=10)
    # 좌석수
    seats_no = models.IntegerField()
    # 소속 영화관
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)


# 상영(Screening) 객체 모델
class Screening(models.Model):
    # 상영 영화
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,)
    # 상영 영화관(theater)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE,)
    # 상영관(auditorium)
    auditorium = models.ForeignKey(Auditorium, on_delete=models.CASCADE)
    # 상영시간
    screening_time = models.DateTimeField()


# 좌석(Seat) 객체 모델
class Seat(models.Model):
    # 좌석 위치(행)
    row = models.CharField(max_length=5)
    # 좌석 위치(열)
    number = models.IntegerField()
    # 배치 상영관
    auditorium = models.ForeignKey(Auditorium, on_delete=models.CASCADE)
    # 예매 여부
    reservation_check = models.BooleanField()


# 예매(Reservation) 객체 모델
class Reservation(models.Model):
    # 예매 유저
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 예매 영화
    # movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    # 예매 극장
    # theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    # 예매 상영 정보(상영관/영화 상영시간)
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE)
    # 예매 좌석 정보
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)


# 이후 reservation_type (ex) 청소년, 일반 ...)을 추가할 수 있다.
# 이 경우는 Reservation에 reservation_type 필드를 추가하고,
# class Reservation_Type(models.Model)을 추가한다.
# Charfield + Choice_Set을 구성한다.(or CHOICE FIELD를 사용)