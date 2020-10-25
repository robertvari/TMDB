from PySide2.QtCore import QObject, Slot, Property, QUrl, Signal
import tmdbsimple as tmdb
from utilities import settings
import os


class MovieDetail(QObject):
    changed = Signal()

    def __init__(self):
        super(MovieDetail, self).__init__()

        self._poster = None
        self._title = None
        self._genres = None
        self._overview = None
        self._released_date = None

    @Slot(int)
    def load(self, movie_id):
        data = tmdb.Movies(movie_id).info()

        self._poster = QUrl().fromLocalFile(os.path.join(settings.CACHE_FOLDER, data["poster_path"][1:]))

        self.changed.emit()

    def _get_poster(self):
        return self._poster

    poster = Property(QUrl, _get_poster, notify=changed)