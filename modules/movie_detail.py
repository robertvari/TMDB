from PySide2.QtCore import QObject, Slot
import tmdbsimple as tmdb


class MovieDetail(QObject):
    def __init__(self):
        super(MovieDetail, self).__init__()

    @Slot(int)
    def load(self, movie_id):
        response = tmdb.Movies(movie_id).info()
