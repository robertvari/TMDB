import tmdbsimple as tmdb
import os

tmdb.API_KEY = os.getenv('TMDB_API_KEY')

if __name__ == '__main__':
    movie = tmdb.Movies()
    result = movie.popular(page=10)

    for i in result["results"]:
        print(i)

    print(result["page"], result['total_pages'], len(result["results"]))