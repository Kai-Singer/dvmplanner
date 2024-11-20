from django.urls import path
from dvmplanner import views

urlpatterns = [
  path('', views.home, name = 'home'),
  path('dashboard/', views.dashboard, name = 'dashboard'),
  path('reports/', views.reports, name = 'reports'),
  path('review/', views.review, name = 'review'),
  path('admin/', views.admin, name = 'admin'),
  path('profile/', views.profile, name = 'profile'),
  path('addreport/', views.addreport, name = 'addreport'),
]