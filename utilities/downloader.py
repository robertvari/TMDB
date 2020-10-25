from utilities import settings
import requests, os, shutil


def download_image(image_url, backdrop=False):
    poster_url = f'{settings.IMAGE_SERVER}{image_url}'
    if backdrop:
        poster_url = f'{settings.IMAGE_BACKDROP_SERVER}{image_url}'

    response = requests.get(poster_url, stream=True)

    if response.status_code == 200:
        poster_file_name = image_url[1:]
        poster_path = os.path.join(settings.CACHE_FOLDER, poster_file_name)

        with open(poster_path, "wb") as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)

    return poster_path