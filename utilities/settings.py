import os

IMAGE_SERVER = 'https://image.tmdb.org/t/p/w300'
IMAGE_BACKDROP_SERVER = 'https://image.tmdb.org/t/p/w1920_and_h800_multi_faces'
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
CACHE_FOLDER = os.path.dirname(__file__).replace("utilities", "_data_cache")
CACHE_FILE = os.path.join(CACHE_FOLDER, "db_data.json")
IMAGES_DIR = os.path.dirname(__file__).replace("utilities", "images")

if __name__ == '__main__':
    print(f"{IMAGE_BACKDROP_SERVER}/5UkzNSOK561c2QRy2Zr4AkADzLT.jpg")