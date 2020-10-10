import tmdbsimple as tmdb
import os

tmdb.API_KEY = os.getenv('TMDB_API_KEY')

if __name__ == '__main__':
    search = tmdb.Search()
    response = search.movie(query='Alien')

    for s in search.results:
        print(s)