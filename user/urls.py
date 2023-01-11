from django.urls import path
from user import views

urlpatterns = [
    path('', views.login_view, name ="login"),
    path('register/', views.register_view, name ="register"),
    path('login/', views.login_view, name ="login"),
    path('logout/', views.logout_view, name ="logout"),
    path('preference_set/<user_id>/', views.preference_set_view, name ="preference_view"),
    path('set_preference', views.preference_submit, name ="set_preference")
]