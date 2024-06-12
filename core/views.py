from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .api import *
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
def index(request):
    movies = top_movies2()[:6]
    series = top_series2()[:6]
    grouped_movies = [movies[i:i+2] for i in range(0, len(movies), 2)]
    grouped_shows = [series[i:i+2] for i in range(0, len(movies), 2)]
    return render(request, 'index.html', {
        'user': request.user,
        'movies': grouped_movies,
        'series':grouped_shows,
    })
    
    
def movie_view(request,id,lang):
    details = movie_checkup(id)
    all_lang = movie_lang(id)
    return render(request,'movie.html',{
        'details':details,
        'image':details['image'],
        'eng_lang':all_lang[1],
        'fr_lang':all_lang[0],
        'lang':lang
    })
    
    
def show_view(request,id,saison=None,lang=None):
    details = show_checkup(id)
    all_lang = show_lang(id)
    episodes = None
    if lang:
        if not saison:
            if lang =='fr':
                saison = french_saison(id)
                        
            else:
                saison = details.get('seasons')
        else:
            if lang =='fr':
                episodes = french_episode(id, saison)
                        
            else:
                episodes = details.get('episodes')
    return render(request,'copy_show.html',{
        'details':details,
        'image':details['image'],
        'id':id,
        'season':saison,
        'ep_data':episodes,
        'eng_lang':all_lang[1],
        'fr_lang':all_lang[0],
        'lang':lang
    })
def stream_show(request,id,saison,ep,lang):
    details = show_checkup(id)
    stream =True
    return render(request,'copy_show.html',{
        'details':details,
        'image':details['image'],
        'season':saison,
        'ep':int(ep),
        'id':id,
        'stream':stream,
        'lang':lang
    })
    
def movie_list_view(request, index=1):
    limit = 12 * int(index)
    movies = top_movies2()[0:limit]
    return render(request,'movie_list.html',{
        'movies':movies,
        'index':int(index)
    })
    
def show_list_view(request, index=1):
    limit = 12 * int(index)
    series = top_series2()[0:limit]
    return render(request,'show_list.html',{
        'series':series,
        'index':int(index)
    })
 
@csrf_exempt    
def search_view(request):
    query = request.POST.get('search')
    search_result = search2(query)
    return render(request,'search_list.html',{
        "result":search_result,
    })
    
def search_genre(request, genre,index=1):
    limit = 6 * int(index)
    movie_list = genre_movies2(movie_genre_list[genre])[0:limit]
    show_list = genre_series2(show_genre_list[genre])[0:limit]
    result = movie_list + show_list
    return render(request,'genre_list.html',{
        "result":result,
        'index':int(index),
        'genre':genre,
    })
    
movie_genre_list = {
    'Action':28,
    'Drama':18,
    'Family':10751,
    'Thriller':53,
    'Comedy':35,
    'Romance':10749,
    'Horror':27
}
show_genre_list = {
    'Action':10759,
    'Drama':18,
    'Family':10751,
    'Thriller':9648,
    'Comedy':35,
    'Romance':80,
    'Horror':10768
}

@api_view(['GET'])
def react_index(request):
    movies = top_movies2()[:2]
    series = top_series2()[:2]
    tops = movies + series
    return Response({
        'tops':tops
    })