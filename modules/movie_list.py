from PySide2.QtCore import QAbstractListModel, QModelIndex, \
    Qt, QRunnable, QObject, QThreadPool, Signal
import tmdbsimple as tmdb
import os

tmdb.API_KEY = os.getenv('TMDB_API_KEY')


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
        movie_data['vote_average'] = movie_data['vote_average'] * 10
        self.insert_movie(movie_data)

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

    def run(self):
        result = self.moviedb_movie.popular()

        for movie_data in result["results"]:
            if not movie_data.get("release_date"):
                continue

            if not movie_data.get("original_title"):
                continue

            if not movie_data.get("popularity"):
                continue

            if not movie_data.get("poster_path"):
                continue

            self.signals.finished.emit(movie_data)