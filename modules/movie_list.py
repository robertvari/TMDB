from PySide2.QtCore import QAbstractListModel, QModelIndex, \
    Qt, QRunnable, QObject, QThreadPool, Signal, QUrl, Property, QSortFilterProxyModel, Slot
import tmdbsimple as tmdb
import os, json, requests, shutil, copy
from datetime import datetime

tmdb.API_KEY = '83cbec0139273280b9a3f8ebc9e35ca9'
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

        self._downloading = False
        self._max_job_count = 0
        self._progress_value = 0

        self._fetch()

    def _fetch(self):
        worker = MovieListWorker()
        worker.signals.job_started.connect(self._job_started)
        worker.signals.progress.connect(self._update_progress)
        worker.signals.job_finished.connect(self._job_finished)
        worker.signals.finished.connect(self.data_finished)
        self.pool.start(worker)

    def _job_started(self, max_count):
        self._downloading = True
        self._max_job_count = max_count
        self.progress_changed.emit()

    def _update_progress(self, value):
        self._progress_value = value
        self.progress_changed.emit()

    def _job_finished(self):
        self._downloading = False
        self.progress_changed.emit()

    def _is_downloading(self):
        return self._downloading

    def _get_job_count(self):
        return self._max_job_count

    def _get_job_progress(self):
        return self._progress_value

    def data_finished(self, movie_data):
        data = copy.copy(movie_data)

        date = datetime.strptime(data["release_date"], '%Y-%m-%d')

        data['vote_average'] = data['vote_average'] * 10
        data['poster_path'] = QUrl().fromLocalFile(os.path.join(CACHE_FOLDER, data['poster_path'][1:]))
        data['display_date'] = date.strftime('%Y %B %d.')
        data['sort_date'] = date
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

    show_progress = Property(bool, _is_downloading, notify=progress_changed)
    max_job_count = Property(int, _get_job_count, notify=progress_changed)
    progress_value = Property(int, _get_job_progress, notify=progress_changed)


class MovieListProxy(QSortFilterProxyModel):
    sort_mode_changed = Signal()

    def __init__(self):
        super(MovieListProxy, self).__init__()
        self.sort(0, Qt.AscendingOrder)

        self._sort_mode = "title"
        self._filter = None

    def _get_mode(self):
        return self._sort_mode

    def _set_mode(self, mode):
        if mode == self._sort_mode:
            if self.sortOrder() == Qt.AscendingOrder:
                self.sort(0, Qt.DescendingOrder)
            else:
                self.sort(0, Qt.AscendingOrder)
        else:
            self.sort(0, Qt.AscendingOrder)

        self._sort_mode = mode
        self.sort_mode_changed.emit()
        self.invalidate()

    def _get_mode(self):
        return self._sort_mode

    def _get_direction(self):
        return self.sortOrder() == Qt.AscendingOrder

    @Slot(str)
    def set_filter(self, value):
        self._filter = value if len(value) else None
        self.invalidateFilter()

    def filterAcceptsRow(self, sourceRow, sourceParent):
        if not self._filter:
            return True

        index = self.sourceModel().index(sourceRow, 0, sourceParent)
        data = index.data(Qt.UserRole)

        if self._filter.lower() in data["title"].lower():
            return True
        return False

    def lessThan(self, left, right):
        left_data = self.sourceModel().data(left, Qt.UserRole)
        right_data = self.sourceModel().data(right, Qt.UserRole)

        return left_data[self._sort_mode] < right_data[self._sort_mode]

    sort_mode = Property(str, _get_mode, _set_mode, notify=sort_mode_changed)
    sort_direction = Property(bool, _get_direction, notify=sort_mode_changed)


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
        self.max_pages = 1

    @staticmethod
    def _check_data(data):
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

                # get poster
                poster_url = f'{IMAGE_SERVER}{movie_data["poster_path"]}'
                response = requests.get(poster_url, stream=True)

                if response.status_code == 200:
                    poster_file_name = movie_data["poster_path"][1:]
                    poster_path = os.path.join(CACHE_FOLDER, poster_file_name)

                    with open(poster_path, "wb") as f:
                        response.raw.decode_content = True
                        shutil.copyfileobj(response.raw, f)

                # get backdrop
                poster_url = f'{IMAGE_SERVER}{movie_data["backdrop_path"]}'
                response = requests.get(poster_url, stream=True)

                if response.status_code == 200:
                    poster_file_name = movie_data['backdrop_path'][1:]
                    poster_path = os.path.join(CACHE_FOLDER, poster_file_name)

                    with open(poster_path, "wb") as f:
                        response.raw.decode_content = True
                        shutil.copyfileobj(response.raw, f)

                self.signals.finished.emit(movie_data)
                self.signals.progress.emit(len(cache_list))

            current_page += 1
            if current_page > result['total_pages']:
                break

        with open(CACHE_FILE, "w") as f:
            json.dump(cache_list, f)

        return cache_list

    @staticmethod
    def _load_cache():
        with open(CACHE_FILE) as f:
            return json.load(f)

    def run(self):
        if os.path.exists(CACHE_FILE):  # get data from cache
            movie_data = self._load_cache()
            self.signals.job_started.emit(len(movie_data))
            for index, data in enumerate(movie_data):
                self.signals.finished.emit(data)
                self.signals.progress.emit(index)

        else:  # download data
            self._cache_data()

        self.signals.job_finished.emit()