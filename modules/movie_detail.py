from PySide2.QtCore import QObject, Slot, Property, QUrl, Signal, QThread
import tmdbsimple as tmdb
from utilities import settings
from utilities.downloader import download_image
import os
from datetime import datetime


class MovieDetail(QObject):
    changed = Signal()
    loader_changed = Signal()

    def __init__(self):
        super(MovieDetail, self).__init__()

        self._poster = None
        self._backdrop = None
        self._title = None
        self._released_date = None
        self._genres = None
        self._tagline = None
        self._runtime = None
        self._overview = None

        self._loading = False

    @Slot(int)
    def load(self, movie_id):
        self._set_loading(True)

        self.worker = GetMovieWorker()
        self.worker.set_movie(movie_id)
        self.worker.finished.connect(self._data_ready)
        self.worker.start()

    def _data_ready(self, data):
        self._poster = QUrl().fromLocalFile(os.path.join(settings.CACHE_FOLDER, data["poster_path"][1:]))
        self._backdrop = QUrl().fromLocalFile(os.path.join(settings.CACHE_FOLDER, data["backdrop_path"][1:]))

        self._title = data["title"]

        date = datetime.strptime(data["release_date"], "%Y-%m-%d")
        self._released_date = date.strftime("%Y %B %d.")

        self._genres = ", ".join([i["name"] for i in data["genres"]])
        self._runtime = data["runtime"]
        self._tagline = data["tagline"]
        self._overview = data["overview"]

        self._set_loading(False)

        self.changed.emit()

    def _set_loading(self, value):
        self._loading = value
        self.loader_changed.emit()

    def _get_poster(self):
        return self._poster

    def _get_backdrop(self):
        return self._backdrop

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

    def _is_loading(self):
        return "loading" if self._loading else "loaded"

    poster = Property(QUrl, _get_poster, notify=changed)
    backdrop = Property(QUrl, _get_backdrop, notify=changed)
    title = Property(str, _get_title, notify=changed)
    date = Property(str, _get_date, notify=changed)
    genres = Property(str, _get_genres, notify=changed)
    runtime = Property(int, _get_runtime, notify=changed)
    tagline = Property(str, _get_tagline, notify=changed)
    overview = Property(str, _get_overview, notify=changed)

    loading = Property(str, _is_loading, notify=loader_changed)


class GetMovieWorker(QThread):
    finished = Signal(dict)

    def __init__(self):
        super(GetMovieWorker, self).__init__()
        self._movie_id = None

    def set_movie(self, movie_id):
        self._movie_id = movie_id

    def _download_backdrop(self, backdrop_path):
        download_image(backdrop_path, backdrop=True)

    def run(self):
        data = tmdb.Movies(self._movie_id).info()
        self._download_backdrop(data['backdrop_path'])

        self.finished.emit(data)
