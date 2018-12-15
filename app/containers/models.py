from django.db import models

# Create your models here.
from mappings.models import Movie


# Dynamic Path for Media File upload_to
def event_directory_path(instance, filename):
    directory = instance.event_name
    return f'{directory}/{filename}'


def trailer_directory_path(instance, filename):
    directory = instance.movie.title
    return f'{directory}/{filename}'


# 메인 이벤트 컨테이너
class MainContainer(models.Model):
    def __str__(self):
        return self.event_name

    class Meta:
        verbose_name = '메인 이벤트(상단) 구성'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['pk']

    event_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='이벤트명')
    posting_start = models.DateTimeField(verbose_name='포스팅 시작')
    posting_end = models.DateTimeField(verbose_name='포스팅 종료')
    container_img = models.ImageField(upload_to=event_directory_path, blank=True, null=True, verbose_name='이벤트 이미지')
    container_link = models.URLField(default='', blank=True, null=True, verbose_name='이벤트 링크')
    is_active = models.BooleanField(default=True, blank=True, null=True, verbose_name='활성화')


# 웹 전용 영화 트레일러 컨테이너(MOVIE SELECTION)
class WebTrailerContainer(models.Model):
    def __str__(self):
        return self.movie.title

    class Meta:
        verbose_name = '웹 영화 트레일러(MOVIE SELECTION)'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['pk']

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='영화')

    # 웹 게시용(큰 사이즈)
    posting_img = models.ImageField(upload_to=trailer_directory_path, blank=True, null=True, verbose_name='영화 이미지')


# 앱 전용 영화 트레일러 컨테이너(MOVIE SELECTION)
class AppTrailerContainer(models.Model):
    def __str__(self):
        return self.movie.title

    class Meta:
        verbose_name = '앱 영화 트레일러(MOVIE SELECTION)'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['pk']

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='영화')

    # 앱 게시용(작은 사이즈)
    comment = models.CharField(max_length=50, blank=True, null=True, verbose_name='코멘트')
    posting_img = models.ImageField(upload_to=trailer_directory_path, blank=True, null=True, verbose_name='영화 이미지')


# 이벤트 컨테이너
class EventContainer(models.Model):
    def __str__(self):
        return self.event_name

    class Meta:
        verbose_name = '이벤트(중단) 구성'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['pk']

    event_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='이벤트명')
    container_img = models.ImageField(upload_to=event_directory_path, blank=True, null=True, verbose_name='이벤트 이미지')
    container_link = models.URLField(default='', blank=True, null=True, verbose_name='이벤트 링크')
    is_active = models.BooleanField(default=True, verbose_name='활성화')


# 하단 이벤트 컨테이너
class EventFooterContainer(models.Model):
    def __str__(self):
        return self.event_name

    class Meta:
        verbose_name = '이벤트(하단) 구성'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['pk']

    event_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='이벤트명')
    container_img = models.ImageField(upload_to=event_directory_path, blank=True, null=True, verbose_name='이벤트 이미지')
    container_link = models.URLField(default='', blank=True, null=True, verbose_name='이벤트 링크')
    is_active = models.BooleanField(default=True, verbose_name='활성화')
