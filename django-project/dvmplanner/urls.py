from django.urls import path
from dvmplanner import views

urlpatterns = [
  path('', views.home, name = 'home')
]