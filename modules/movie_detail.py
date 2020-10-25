from PySide2.QtCore import QObject, Slot, Property, QUrl, Signal
import tmdbsimple as tmdb
from utilities import settings
import os
from datetime import datetime


class MovieDetail(QObject):
    changed = Signal()

    def __init__(self):
        super(MovieDetail, self).__init__()

        self._poster = None
        self._title = None
        self._released_date = None
        self._genres = None
        self._tagline = None
        self._runtime = None
        self._overview = None

    @Slot(int)
    def load(self, movie_id):
        data = tmdb.Movies(movie_id).info()

        self._poster = QUrl().fromLocalFile(os.path.join(settings.CACHE_FOLDER, data["poster_path"][1:]))
        self._title = data["title"]

        date = datetime.strptime(data["release_date"], "%Y-%m-%d")
        self._released_date = date.strftime("%Y %B %d.")

        self._genres = ", ".join([i["name"] for i in data["genres"]])
        self._runtime = data["runtime"]
        self._tagline = data["tagline"]
        self._overview = data["overview"]

        self.changed.emit()

    def _get_poster(self):
        return self._poster

    def _get_title(self):
        return self._title

    def _get_date(self):
        return self._released_date

    def _get_genres(self):
        return self._genres

    def _get_runtime(self):
        return self._runtime

    def _get_tagline(self):
        return self._tagline

    def _get_overview(self):
        return self._overview

    poster = Property(QUrl, _get_poster, notify=changed)
    title = Property(str, _get_title, notify=changed)
    date = Property(str, _get_date, notify=changed)
    genres = Property(str, _get_genres, notify=changed)
    runtime = Property(int, _get_runtime, notify=changed)
    tagline = Property(str, _get_tagline, notify=changed)
    overview = Property(str, _get_overview, notify=changed)