from PySide2.QtCore import QAbstractListModel, QModelIndex, Qt


class MovieList(QAbstractListModel):
    DataRole = Qt.UserRole

    def __init__(self):
        super(MovieList, self).__init__()
        self.items = []

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