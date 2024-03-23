from django.urls import path
from .views import WeekTop,MovieLookup

urlpatterns = [
    path('week-top',WeekTop.as_view())
]
