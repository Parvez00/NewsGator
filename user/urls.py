from django.urls import path
from user import views

urlpatterns = [
    path('register/', views.register_view, name ="register"),
    path('login/', views.login_view, name ="login"),
    path('logout/', views.logout_view, name ="logout"),
    path('set_preference', views.preference_submit, name ="set_preference")
]