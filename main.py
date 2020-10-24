# This Python file uses the following encoding: utf-8
import sys
import os

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine

from modules.movie_list import MovieList, MovieListProxy
from modules.movie_details import MovieDetails


class Main:
    def __init__(self):
        self.app = QGuiApplication(sys.argv)
        self.engine = QQmlApplicationEngine()
        self.context = self.engine.rootContext()

        self._setup_context()

        self.engine.load(os.path.join(os.path.dirname(__file__), "main.qml"))

        if not self.engine.rootObjects():
            sys.exit(-1)
        sys.exit(self.app.exec_())

    def _setup_context(self):
        self.movie_list = MovieList()
        self.context.setContextProperty("MovieList", self.movie_list)

        self.movie_list_proxy = MovieListProxy()
        self.movie_list_proxy.setSourceModel(self.movie_list)
        self.context.setContextProperty("MovieListProxy", self.movie_list_proxy)

        self.movie_details = MovieDetails()
        self.context.setContextProperty("MovieDetails", self.movie_details)


if __name__ == "__main__":
    Main()
