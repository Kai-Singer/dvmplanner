from django.urls import path
from dvmplanner import views

urlpatterns = [
  path('', views.dashboard, name = 'dashboard')
]