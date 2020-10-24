from PySide2.QtCore import QAbstractListModel, QModelIndex, \
    Qt, QRunnable, QObject, QThreadPool, Signal, QUrl
import tmdbsimple as tmdb
import os, json, requests, shutil, copy

tmdb.API_KEY = os.getenv('TMDB_API_KEY')
IMAGE_SERVER = 'https://image.tmdb.org/t/p/w300'
CACHE_FOLDER = os.path.dirname(__file__).replace("modules", "_data_cache")
CACHE_FILE = os.path.join(CACHE_FOLDER, "db_data.json")


class MovieList(QAbstractListModel):
    DataRole = Qt.UserRole

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

    def insert_movie(self, movie_data):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.items.append(movie_data)
        self.endInsertRows()

    def edit_item(self, row, movie_data):
        pass

    def delete_item(self, row):
        pass

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


class WorkerSignals(QObject):
    finished = Signal(dict)

    def __init__(self):
        super(WorkerSignals, self).__init__()


class MovieListWorker(QRunnable):
    def __init__(self):
        super(MovieListWorker, self).__init__()
        self.signals = WorkerSignals()
        self.moviedb_movie = tmdb.Movies()

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

        with open(CACHE_FILE, "w") as f:
            json.dump(cache_list, f)

    def run(self):
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE) as f:
                movie_data = json.load(f)

                for data in movie_data:
                    self.signals.finished.emit(data)
        else:
            self._cache_data()