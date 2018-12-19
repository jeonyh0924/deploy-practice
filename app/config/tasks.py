


from config.celery import app
from mappings.models import ReservedSeat, Screening


@app.task
def makereservation(screen_pk):
    screen = Screening.objects.get(pk=screen_pk)
    movie_pk = screen.movie.pk
    screen.movie.reservation_score = len(ReservedSeat.objects.filter(screening__movie__pk=movie_pk)) / len(ReservedSeat.objects.all())
    screen.movie.save()
