from PySide2.QtCore import QObject, Property, QUrl, Signal, Slot
import tmdbsimple as tmdb
import os

tmdb.API_KEY = os.getenv('TMDB_API_KEY')
IMAGE_SERVER = 'https://image.tmdb.org/t/p/w300'
CACHE_FOLDER = os.path.dirname(__file__).replace("modules", "_data_cache")


class MovieDetails(QObject):
    changed = Signal()

    def __init__(self):
        super(MovieDetails, self).__init__()
        self._poster = None
        self._title = None
        self._rating = None
        self._overview = None
        self._language = None

    @Slot(int)
    def load(self, movie_id):
        response = tmdb.Movies(movie_id).info()
        self._title = response["title"]
        self._poster = QUrl().fromLocalFile(os.path.join(CACHE_FOLDER, response["poster_path"][1:]))
        self._overview = response["overview"]
        self.changed.emit()

    def _get_poster(self):
        return self._poster

    def _get_title(self):
        return self._title

    def _get_overview(self):
        return self._overview

    poster = Property(QUrl, _get_poster, notify=changed)
    title = Property(str, _get_title, notify=changed)
    overview = Property(str, _get_overview, notify=changed)