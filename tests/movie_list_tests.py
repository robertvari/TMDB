import unittest
import tmdbsimple as tmdb
import os, json, requests, shutil

tmdb.API_KEY = os.getenv('TMDB_API_KEY')
image_server = 'https://image.tmdb.org/t/p/w300'
movie = tmdb.Movies()

data_cache_folder = os.path.dirname(__file__).replace("tests", "_data_cache")


class MovieListTests(unittest.TestCase):

    def test_cache_movie(self):
        if not os.path.exists(data_cache_folder):
            os.mkdir(data_cache_folder)

        data_dict = {}
        data_file_name = f"db_data.json"
        file_path = os.path.join(data_cache_folder, data_file_name)

        # check if we have data cached
        if os.path.exists(file_path):
            with open(file_path) as f:
                movie_data = json.load(f)
                print(movie_data)
        else:
            result = movie.popular()

            for i in result["results"]:
                poster_url = f'{image_server}{i["poster_path"]}'
                response = requests.get(poster_url, stream=True)

                if response.status_code == 200:
                    poster_file_name = i["poster_path"][1:]
                    poster_path = os.path.join(data_cache_folder, poster_file_name)

                    with open(poster_path, "wb") as f:
                        response.raw.decode_content = True
                        shutil.copyfileobj(response.raw, f)

                data_dict[i["id"]] = i


            with open(file_path, "w") as f:
                json.dump(data_dict, f)