from django.urls import path
from .views import react_index,index,movie_view,show_view,stream_show,movie_list_view,show_list_view,search_view,search_genre

urlpatterns = [
    path('',index, name='index'),
    path('api',react_index, name='react'),
    path('search',search_view, name='search'),
    path('search_list/<str:index>/<str:genre>',search_genre, name='genre'),
    path('movie_list/<str:index>',movie_list_view, name='movie_list'),
    path('tv_list/<str:index>',show_list_view, name='tv_list'),
    path('movie/<str:id>/<str:lang>',movie_view, name='movie'),
    path('show/<str:id>/',show_view, name='show_language'),
    path('show/<str:id>/<str:lang>',show_view, name='show_season'),
    path('show/<str:id>/<int:saison>/<str:lang>',show_view, name='show_ep'),
    path('watch/<str:id>/<int:saison>/<int:ep>/<str:lang>',stream_show, name='stream'),
]
