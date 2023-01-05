from django.urls import path
from user import views

urlpatterns = [
    path('register/', views.register_view, name ="register")
]