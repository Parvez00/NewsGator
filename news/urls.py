from django.urls import path
from news import views


urlpatterns = [
    path('news_scrap/<domain>/', views.news_scrap, name ="news"),
    path('user_home/<user_id>/', views.user_home_view, name ="home")
]