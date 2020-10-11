from PySide2.QtCore import QAbstractListModel, QModelIndex, Qt


class MovieList(QAbstractListModel):
    DataRole = Qt.UserRole

    def __init__(self):
        super(MovieList, self).__init__()
        self.items = []
        self.current_page = 1

        self._fetch()

    def _fetch(self):
        for i in range(20):
            movie_data = {
                "movie_id": i,
                "original_title": "Star Wars",
                "poster_path": "../images/vfrQk5IPloGg1v9Rzbh2Eg3VGyM.jpg",
                "popularity": 80,
                "release_date": "1977-05-25"
            }
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