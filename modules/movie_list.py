from PySide2.QtCore import QAbstractListModel, QModelIndex, \
    Qt, QRunnable, QObject, QThreadPool, Signal, QUrl, Property
import tmdbsimple as tmdb
import os, json, requests, shutil, copy, time

tmdb.API_KEY = os.getenv('TMDB_API_KEY')
IMAGE_SERVER = 'https://image.tmdb.org/t/p/w300'
CACHE_FOLDER = os.path.dirname(__file__).replace("modules", "_data_cache")
CACHE_FILE = os.path.join(CACHE_FOLDER, "db_data.json")


class MovieList(QAbstractListModel):
    DataRole = Qt.UserRole
    progress_changed = Signal()

    def __init__(self):
        super(MovieList, self).__init__()
        self.items = []
        self.current_page = 1
        self.pool = QThreadPool()
        self.pool.setMaxThreadCount(1)

        self._fetch()

    def _fetch(self):
        worker = MovieListWorker()
        worker.signals.finished.connect(self.data_finished)
        self.pool.start(worker)

    def data_finished(self, movie_data):
        data = copy.copy(movie_data)

        data['vote_average'] = data['vote_average'] * 10
        data['poster_path'] = QUrl().fromLocalFile(os.path.join(CACHE_FOLDER, data["poster_path"][1:]))
        self.insert_movie(data)
        self.progress_changed.emit()

    def insert_movie(self, movie_data):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.items.append(movie_data)
        self.endInsertRows()

    def rowCount(self, parent=QModelIndex):
        return len(self.items)

    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        if role == MovieList.DataRole:
            return self.items[row]

    def roleNames(self):
        return {
            MovieList.DataRole: b'movie_item'
        }

    progress_value = Property(int, _get_job_progress, notify=progress_changed)


class WorkerSignals(QObject):
    finished = Signal(dict)
    job_started = Signal(int)
    progress = Signal(int)
    job_finished = Signal()

    def __init__(self):
        super(WorkerSignals, self).__init__()


class MovieListWorker(QRunnable):
    def __init__(self):
        super(MovieListWorker, self).__init__()
        self.signals = WorkerSignals()
        self.moviedb_movie = tmdb.Movies()
        self.max_pages = 10

    def _check_data(self, data):
        if not data.get("release_date"):
            return False

        if not data.get("original_title"):
            return False

        if not data.get("vote_average"):
            return False

        if not data.get("poster_path"):
            return False

        return True

    def _cache_data(self):
        if not os.path.exists(CACHE_FOLDER):
            os.makedirs(CACHE_FOLDER)

        current_page = 1
        cache_list = []

        self.signals.job_started.emit(self.max_pages * 20)
        while current_page <= self.max_pages:
            result = self.moviedb_movie.popular(page=current_page)
            for movie_data in result["results"]:
                if not self._check_data(movie_data):
                    continue

                cache_list.append(movie_data)

                # download poster
                poster_url = f'{IMAGE_SERVER}{movie_data["poster_path"]}'
                response = requests.get(poster_url, stream=True)

                if response.status_code == 200:
                    poster_file_name = movie_data["poster_path"][1:]
                    poster_path = os.path.join(CACHE_FOLDER, poster_file_name)

                    with open(poster_path, "wb") as f:
                        response.raw.decode_content = True
                        shutil.copyfileobj(response.raw, f)

                self.signals.finished.emit(movie_data)
                self.signals.progress.emit(len(cache_list))

            current_page += 1
            if current_page > result["total_pages"]:
                break

        with open(CACHE_FILE, "w") as f:
            json.dump(cache_list, f)

    def run(self):
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE) as f:
                movie_data = json.load(f)

                self.signals.job_started.emit(len(movie_data))
                for index, data in enumerate(movie_data):
                    time.sleep(1)
                    self.signals.finished.emit(data)
                    self.signals.progress(index)
        else:
            self._cache_data()

        self.signals.job_finished()