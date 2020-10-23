from PySide2.QtCore import QObject, Property, QUrl, Signal, Slot, QThread
import tmdbsimple as tmdb
import os

tmdb.API_KEY = os.getenv('TMDB_API_KEY')
IMAGE_SERVER = 'https://image.tmdb.org/t/p/w300'
CACHE_FOLDER = os.path.dirname(__file__).replace("modules", "_data_cache")


class MovieDetails(QObject):
    changed = Signal()
    loader_changed = Signal()

    def __init__(self):
        super(MovieDetails, self).__init__()
        self.worker = GetMovieWorker()

        self._poster = None
        self._title = None
        self._rating = None
        self._overview = None
        self._language = None

        self._loding = False

    @Slot(int)
    def load(self, movie_id):
        self._set_loading(True)

        self.worker.set_movie(movie_id)
        self.worker.finished.connect(self._data_ready)
        self.worker.start()

    def _data_ready(self, data):
        self._title = data["title"]
        self._poster = QUrl().fromLocalFile(os.path.join(CACHE_FOLDER, data["poster_path"][1:]))
        self._overview = data["overview"]
        self.changed.emit()
        self._set_loading(False)

    def _set_loading(self, value):
        self._loding = value
        self.loader_changed.emit()

    def _is_loading(self):
        return "loading" if self._loding else "loaded"

    def _get_poster(self):
        return self._poster

    def _get_title(self):
        return self._title

    def _get_overview(self):
        return self._overview

    poster = Property(QUrl, _get_poster, notify=changed)
    title = Property(str, _get_title, notify=changed)
    overview = Property(str, _get_overview, notify=changed)

    loading = Property(str, _is_loading, notify=loader_changed)


class GetMovieWorker(QThread):
    finished = Signal(dict)

    def __init__(self):
        super(GetMovieWorker, self).__init__()
        self._movie_id = None

    def set_movie(self, movie_id):
        self._movie_id = movie_id

    def run(self):
        response = tmdb.Movies(self._movie_id).info()
        self.finished.emit(response)