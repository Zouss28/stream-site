import requests
from django.core.cache import cache
from PyMovieDb import IMDB
import ast
import json
import requests
import re

imdb = IMDB()

headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "bf2d1d09e9msh723cd4433c78ed0p153f3ejsn00142a3f5265",
	"X-RapidAPI-Host": "imdb188.p.rapidapi.com"
}


def top_movies():
    cache_key = 'api_top_movies'
    cache_time = 86400  # time to live in seconds for cache, 24 hours

    # Try to get cached data
    movies = cache.get(cache_key)
    
    if not movies:
        res = imdb.popular_movies(genre=None, start_id=1, sort_by=None)
        res = ast.literal_eval(res)
        data = res["results"]

        # Extracting required fields
        movies = []
        for item in data:
            extracted_item = {
                "id": item.get("id", "N/A"),
                "title": item.get("name", {}),
                "rating": item.get("ratingsSummary", {}),
                "description": item.get("plot", {}),
                "image": item.get("poster", {}),
                "year":item.get('year', 'N/A')
            }
            movies.append(extracted_item)
        cache.set(cache_key, movies, cache_time)
        
    return movies
        

def top_series():
    cache_key = 'api_top_shows'
    cache_time = 86400  # time to live in seconds for cache, 24 hours

    # Try to get cached data
    series = cache.get(cache_key)
    
    if not series:
        res = imdb.popular_tv(genre=None, start_id=1, sort_by=None)
        res = ast.literal_eval(res)
        data = res["results"]

        # Extracting required fields
        series = []
        for item in data:
            extracted_item = {
                "id": item.get("id", "N/A"),
                "title": item.get("name", {}),
                "rating": item.get("ratingsSummary", {}),
                "description": item.get("plot", {}),
                "image": item.get("poster", {}),
                "year":item.get('year', 'N/A')
            }
            series.append(extracted_item)
        cache.set(cache_key, series, cache_time)
    
    return series

def movie_checkup(id):
    res = imdb.get_by_id(id)
    data = json.loads(res)
    detail = {
            'title':data.get('name', 'N/A'),
            'description':data.get('description','N/A'),
            'year':data.get('datePublished'),
            'imdb_rating':round(float(data.get('rating',{}).get('ratingValue','0'))),
            'genre':",".join(data.get('genre',['N,A'])) if isinstance(data.get('genre'), list) else 'N/A',
            'id':id,
            'stars':"Work on it Later",
            'directors':"Work on it Later",
            'countries':",".join(data.get('countries',['N/A'])),
            'image':data.get('poster')
        }
    return detail


def show_checkup(id):
    res = imdb.get_by_id(id)
    data = json.loads(res)
    detail = {
            'title':data.get('name', 'N/A'),
            'description':data.get('description','N/A'),
            'year':data.get('datePublished'),
            'imdb_rating':round(float(data.get('rating','0').get('ratingValue','0'))),
            'genre':",".join(data.get('genre',['N,A'])) if isinstance(data.get('genre'), list) else 'N/A',
            'id':id,
            'stars':"Work on it Later",
            'directors':"Work on it Later",
            'countries':",".join(data.get('countries',['N/A'])),
            'image':data.get('poster')
        }
    return detail


def image_movie_checkup(id):

    url = "https://movies-tv-shows-database.p.rapidapi.com/"

    querystring = {"movieid":id}

    headers = {
	"Type": "get-movies-images-by-imdb",
	"X-RapidAPI-Key": "cfd592575amsh0e68d98d2898c50p1794e3jsn4872a6b809a5",
	"X-RapidAPI-Host": "movies-tv-shows-database.p.rapidapi.com"
}
    try:
        response = requests.get(url, headers=headers, params=querystring)
        
        data = response.json()
        image = data.get('poster','N/A')
    except requests.exceptions.RequestException as e:
        image = []
        
    return image


def image_show_checkup(id):

    url = "https://movies-tv-shows-database.p.rapidapi.com/"

    querystring = {"seriesid":id}

    headers = {
	"Type": "get-show-images-by-imdb",
	"X-RapidAPI-Key": "cfd592575amsh0e68d98d2898c50p1794e3jsn4872a6b809a5",
	"X-RapidAPI-Host": "movies-tv-shows-database.p.rapidapi.com"
}
    try:
        response = requests.get(url, headers=headers, params=querystring)
        
        data = response.json()
        image = data.get('poster','N/A')
    except requests.exceptions.RequestException as e:
        image = []
        
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
        seasons = data.get('tv_seasons','N/A')
        id = data.get('imdb_id', 'N/A')
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
    res = imdb.popular_movies(genre=genre, start_id=1, sort_by=None)
    res = ast.literal_eval(res)
    data = res["results"]

    # Extracting required fields
    movies = []
    for item in data:
        extracted_item = {
            "id": item.get("id", "N/A"),
            "title": item.get("name", {}),
            "rating": item.get("ratingsSummary", {}),
            "description": item.get("plot", {}),
            "image": item.get("poster", {}),
            "year":item.get('year', 'N/A')
        }
        movies.append(extracted_item)
    
    return movies

def genre_series(genre=None):

    res = imdb.popular_tv(genre=genre, start_id=1, sort_by=None)
    res = ast.literal_eval(res)
    data = res["results"]

    # Extracting required fields
    series = []
    for item in data:
        extracted_item = {
            "id": item.get("id", "N/A"),
            "title": item.get("name", {}),
            "rating": item.get("ratingsSummary", {}),
            "description": item.get("plot", {}),
            "image": item.get("poster", {}),
            "year":item.get('year', 'N/A')
        }
        series.append(extracted_item)

    return series

def movie_lang(id):
    fr_url = f"https://api.frembed.fun/movies/check?id={id}"
    response = requests.get(fr_url).json().get('result')
    
    fr_lang = response.get('Total') > 0
    
    eng_url = f"https://vidsrc.xyz/embed/movie/{id}"
    response = requests.get(eng_url).status_code
    eng_lang = response == 200
    
    return(fr_lang,eng_lang)


def show_lang(id):
    fr_url = f"https://api.frembed.fun/tv/check?id={id}"
    response = requests.get(fr_url).json().get('result')
    
    fr_lang = int(response.get('totalItems')) > 0
    
    eng_url = f"https://vidsrc.xyz/embed/tv/{id}"
    response = requests.get(eng_url).status_code
    eng_lang = response == 200
    
    return(fr_lang,eng_lang)

def french_saison(id):
    fr_url = f"https://api.frembed.fun/tv/check?id={id}"
    data = requests.get(fr_url).json()
    seasons = {item['sa'] for item in data['result']['items']}
    no_french_sa = len(seasons)
    return no_french_sa

def french_episode(id, saison):
    fr_url = f"https://api.frembed.fun/tv/check?id={id}&sa={saison}"
    data = requests.get(fr_url).json().get('result')
    ep = data.get('totalItems')
    return int(ep)
    
