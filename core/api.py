import functools
import requests
from django.core.cache import cache
from PyMovieDb import IMDB
import json

imdb = IMDB()

headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": "bf2d1d09e9msh723cd4433c78ed0p153f3ejsn00142a3f5265",
    "X-RapidAPI-Host": "imdb188.p.rapidapi.com"
}

CACHE_EXPIRATION = 86400  # 24 hours

@functools.lru_cache(maxsize=128)
def get_api_data(func, *args, **kwargs):
    response = func(*args, **kwargs)
    print(response)
    return response.json()

@functools.lru_cache(maxsize=128)
def get_python_api_data(func, *args, **kwargs):
    response = func(*args, **kwargs)
    return json.loads(response)

@functools.lru_cache(maxsize=128)
def get_movie_details(movie_id):
    res = imdb.get_by_id(movie_id)
    data = json.loads(res)
    print(res,movie_id)
    return {
        'title': data.get('name', 'N/A'),
        'description': data.get('description', 'N/A'),
        'year': data.get('datePublished'),
        'imdb_rating': round(float(data.get('rating', {}).get('ratingValue', 0))),
        'genre': ','.join(data.get('genre', ['N/A'])) if isinstance(data.get('genre'), list) else 'N/A',
        'id': movie_id,
        'actors':data.get('actor',[]),
        'directors': data.get('director',[]),
        'countries': ','.join(data.get('countries', ['N/A'])),
        'image': data.get('poster')
    }

@functools.lru_cache(maxsize=128)
def get_show_details(show_id):
    res = imdb.get_by_id(show_id)
    data = json.loads(res)
    return {
        'title': data.get('name', 'N/A'),
        'description': data.get('description', 'N/A'),
        'year': data.get('datePublished'),
        'imdb_rating': round(float(data.get('rating', {}).get('ratingValue', 0))),
        'genre': ','.join(data.get('genre', ['N/A'])) if isinstance(data.get('genre'), list) else 'N/A',
        'id': show_id,
        'actors':data.get('actor',[]),
        'directors': data.get('director',[]),
        'countries': ','.join(data.get('countries', ['N/A'])),
        'image': data.get('poster')
    }

def top_movies():
    cache_key = 'api_top_movies'
    movies = cache.get(cache_key)
    if not movies:
        res = get_python_api_data(imdb.popular_movies, genre=None, start_id=1, sort_by=None)
        movies = [
            {
                "id": item.get("id", "N/A"),
                "title": item.get("name", "N/A"),
                "rating": item.get("ratingsSummary", {}),
                "description": item.get("plot", "N/A"),
                "image": item.get("poster", {}),
                "year": item.get('year', 'N/A')
            }
            for item in res["results"]
        ]
        cache.set(cache_key, movies, CACHE_EXPIRATION)
    return movies

def top_series():
    cache_key = 'api_top_shows'
    series = cache.get(cache_key)
    if not series:
        res = get_python_api_data(imdb.popular_tv, genre=None, start_id=1, sort_by=None)
        series = [
            {
                "id": item.get("id", "N/A"),
                "title": item.get("name", "N/A"),
                "rating": item.get("ratingsSummary", {}),
                "description": item.get("plot", "N/A"),
                "image": item.get("poster", {}),
                "year": item.get('year', 'N/A')
            }
            for item in res["results"]
        ]
        cache.set(cache_key, series, CACHE_EXPIRATION)
    return series

def movie_checkup(movie_id):
    return get_movie_details(movie_id)

def show_checkup(show_id):
    return get_show_details(show_id)

def image_movie_checkup(movie_id):
    url = "https://movies-tv-shows-database.p.rapidapi.com/"
    querystring = {"movieid": movie_id}
    headers = {
        "Type": "get-movies-images-by-imdb",
        "X-RapidAPI-Key": "cfd592575amsh0e68d98d2898c50p1794e3jsn4872a6b809a5",
        "X-RapidAPI-Host": "movies-tv-shows-database.p.rapidapi.com"
    }
    try:
        response = get_api_data(requests.get, url, headers=headers, params=querystring)
        image = response.get('poster', 'N/A')
    except requests.exceptions.RequestException:
        image = 'N/A'
    return image

def image_show_checkup(show_id):
    url = "https://movies-tv-shows-database.p.rapidapi.com/"
    querystring = {"seriesid": show_id}
    headers = {
        "Type": "get-show-images-by-imdb",
        "X-RapidAPI-Key": "cfd592575amsh0e68d98d2898c50p1794e3jsn4872a6b809a5",
        "X-RapidAPI-Host": "movies-tv-shows-database.p.rapidapi.com"
    }
    try:
        response = get_api_data(requests.get, url, headers=headers, params=querystring)
        image = response.get('poster', 'N/A')
    except requests.exceptions.RequestException:
        image = 'N/A'
    return image


def show_season(id):

    url = "https://movies-tv-shows-database.p.rapidapi.com/"

    querystring = {"seriesid":id}

    headers = {
	"Type": "get-show-seasons",
	"X-RapidAPI-Key": "6eec8d53cbmsh39a6e3a727c453bp11da8bjsn4944d66ad385",
	"X-RapidAPI-Host": "movies-tv-shows-database.p.rapidapi.com"
}
    try:
        response = requests.get(url, headers=headers, params=querystring)
        
        data = response.json()
        seasons = data.get('tv_seasons',[])
    except requests.exceptions.RequestException as e:
        seasons = []
        
    return len(seasons)

def show_episode(id, season):

    url = "https://movies-tv-shows-database.p.rapidapi.com/"

    querystring = {"seriesid":id,"season":season}

    headers = {
	"Type": "get-show-season-episodes",
	"X-RapidAPI-Key": "6eec8d53cbmsh39a6e3a727c453bp11da8bjsn4944d66ad385",
	"X-RapidAPI-Host": "movies-tv-shows-database.p.rapidapi.com"
}
    try:
        response = requests.get(url, headers=headers, params=querystring)
        
        data = response.json()
        episodes = data.get('tv_episodes',[])
    except requests.exceptions.RequestException as e:
        episodes = []
        
    return len(episodes)

@functools.lru_cache(maxsize=128)
def search_chekup(query):
    query = query.replace(" ", "")
    url = "https://imdb188.p.rapidapi.com/api/v1/searchIMDB"

    querystring = {"query":query}

    headers = {
	"X-RapidAPI-Key": "cfd592575amsh0e68d98d2898c50p1794e3jsn4872a6b809a5",
	"X-RapidAPI-Host": "imdb188.p.rapidapi.com"
}
    try:
        response = requests.get(url, headers=headers, params=querystring)
        
        data = response.json().get('data')
        search_result = []
        for item in data:
            if item.get('qid') is not None :
                extracted_item = {
                    "id": item.get("id", "N/A"),
                    "qid":item.get('qid', 'N/A'),
                    "title": item.get("title", {}),
                    "image": item.get("image", {}),
                    "year":item.get("year",{})
                }
                search_result.append(extracted_item)
                
    except requests.exceptions.RequestException as e:
        search_result = []
    return search_result

def genre_movies(genre=None):
    res = get_python_api_data(imdb.popular_movies, genre=genre, start_id=1, sort_by=None)
    return [
        {
            "id": item.get("id", "N/A"),
            "title": item.get("name", "N/A"),
            "rating": item.get("ratingsSummary", {}),
            "description": item.get("plot", "N/A"),
            "image": item.get("poster", {}),
            "year": item.get('year', 'N/A')
        }
        for item in res["results"]
    ]

def genre_series(genre=None):
    res = get_python_api_data(imdb.popular_tv, genre=genre, start_id=1, sort_by=None)
    return [
        {
            "id": item.get("id", "N/A"),
            "title": item.get("name", "N/A"),
            "rating": item.get("ratingsSummary", {}),
            "description": item.get("plot", "N/A"),
            "image": item.get("poster", {}),
            "year": item.get('year', 'N/A')
        }
        for item in res["results"]
    ]

def movie_lang(movie_id):
    fr_url = f"https://api.frembed.fun/movies/check?id={movie_id}"
    fr_response = get_api_data(requests.get, fr_url)
    fr_lang = fr_response.get('result', {}).get('Total', 0) > 0

    eng_url = f"https://vidsrc.xyz/embed/movie/{movie_id}"
    eng_response = requests.get(eng_url)
    eng_lang = eng_response.status_code == 200

    return fr_lang, eng_lang

def show_lang(show_id):
    fr_url = f"https://api.frembed.fun/tv/check?id={show_id}"
    fr_response = get_api_data(requests.get, fr_url)
    fr_lang = int(fr_response.get('result', {}).get('totalItems', 0)) > 0

    eng_url = f"https://vidsrc.xyz/embed/tv/{show_id}"
    eng_response = requests.get(eng_url)
    eng_lang = eng_response.status_code == 200

    return fr_lang, eng_lang

def french_saison(show_id):
    fr_url = f"https://api.frembed.fun/tv/check?id={show_id}"
    data = get_api_data(requests.get, fr_url)
    seasons = {item['sa'] for item in data.get('result', {}).get('items', [])}
    return len(seasons)

def french_episode(show_id, season):
    fr_url = f"https://api.frembed.fun/tv/check?id={show_id}&sa={season}"
    data = get_api_data(requests.get, fr_url)
    episodes = data.get('result', {}).get('totalItems', 0)
    return int(episodes)