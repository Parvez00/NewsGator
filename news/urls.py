from django.urls import path
from news import views


urlpatterns = [
    path('scrap_news/<domain>/', views.news_scrap, name ="news")
]