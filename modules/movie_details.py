from PySide2.QtCore import QObject, Property, QUrl, Signal, Slot, QThread
import tmdbsimple as tmdb
import os

tmdb.API_KEY = '83cbec0139273280b9a3f8ebc9e35ca9'
IMAGE_SERVER = 'https://image.tmdb.org/t/p/w300'
CACHE_FOLDER = os.path.dirname(__file__).replace("modules", "_data_cache")


class MovieDetails(QObject):
    changed = Signal()
    loader_changed = Signal()

    def __init__(self):
        super(MovieDetails, self).__init__()
        self.worker = GetMovieWorker()

        self._title = None
        self._tagline = None
        self._vote_average = None
        self._poster = None
        self._backdrop = None
        self._genres = None
        self._genres = None
        self._language = None
        self._overview = None
        self._release_date = None
        self._language = None
        self._runtime = None

        self._loding = False

    @Slot(int)
    def load(self, movie_id):
        self._set_loading(True)

        self.worker.set_movie(movie_id)
        self.worker.finished.connect(self._data_ready)
        self.worker.start()

    def _data_ready(self, data):
        self._title = data["title"]
        self._tagline = data['tagline']
        self._vote_average = data['vote_average'] * 10
        self._poster = QUrl().fromLocalFile(os.path.join(CACHE_FOLDER, data["poster_path"][1:]))
        self._backdrop = QUrl().fromLocalFile(os.path.join(CACHE_FOLDER, data["backdrop_path"][1:]))
        self._genres = "/".join([i['name'] for i in data['genres']])
        self._language = data['original_language']
        self._overview = data["overview"]
        self._release_date = data['release_date']
        self._runtime = data['runtime']

        self.changed.emit()
        self._set_loading(False)

    def _set_loading(self, value):
        self._loding = value
        self.loader_changed.emit()

    def _is_loading(self):
        return "loading" if self._loding else "loaded"

    def _get_poster(self):
        return self._poster

    def _get_backdrop(self):
        return self._backdrop

    def _get_date(self):
        return self._release_date

    def _get_title(self):
        return self._title

    def _get_tagline(self):
        return self._tagline

    def _get_genres(self):
        return self._genres

    def _get_language(self):
        return self._language

    def _get_runtime(self):
        return self._runtime

    def _get_overview(self):
        return self._overview

    poster = Property(QUrl, _get_poster, notify=changed)
    backdrop = Property(QUrl, _get_backdrop, notify=changed)
    title = Property(str, _get_title, notify=changed)
    tagline = Property(str, _get_tagline, notify=changed)
    overview = Property(str, _get_overview, notify=changed)
    release_date = Property(str, _get_date, notify=changed)
    genres = Property(str, _get_genres, notify=changed)
    language = Property(str, _get_language, notify=changed)
    runtime = Property(int, _get_runtime, notify=changed)

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