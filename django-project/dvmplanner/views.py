from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles import finders
from dvmplanner.scripts.users import User
import os

uid = 'u0000'
if not finders.find(f'profiles/{uid}.png'):
  uid = '_default'

def home(request):
  return redirect(dashboard)

def dashboard(request):
  # usernames = []
  # users = User.getUsers()
  # for user in users:
  #   usernames.append(user.getUsername())
  # data = {
  #   'usernames': usernames
  # }
  data = {
    'uid': uid,
    'username': 'testuser',
    'first_name': 'Max',
    'last_name': 'Mustermann',
  }
  return render(request, 'dvmplanner/dashboard.html', data)

def reports(request):
  '''
  Important Notes:
  - Wenn Endzeit ein neuer Tag ist -> 'end_day' befüllen, ansonsten leer lassen
  - Wenn Notizen länger als Anzahl Buchstaben -> verkürzte version in 'notes' und lange in 'long_notes', ansonsten 'long_notes' leer lassen
  '''
  data = {
    'uid': uid,
    'username': 'testuser',
    'role': 'vip',
    'reports': [
      {
        'day': '21.11.2024',
        'start': '10.12:43 Uhr',
        'end': '12.58:26 Uhr',
        'end_day': '',
        'time': '2:45:43',
        'module': '1.3.1 Betriebs- und Kommunikationssysteme',
        'notes': 'Weitergearbeitet am Proj...',
        'long_notes': 'Weitergearbeitet am Projekt. Viel Fortschritt!'
      },
      {
        'day': '21.11.2024',
        'start': '10.12:43 Uhr',
        'end': '12.58:26 Uhr',
        'end_day': '22.11.2024',
        'time': '2:45:43',
        'module': '1.3.1 Betriebs- und Kommunikationssysteme',
        'notes': 'Weitergearbeitet am Projekt',
        'long_notes': ''
      },
      {
        'day': '21.11.2024',
        'start': '10.12:43 Uhr',
        'end': '12.58:26 Uhr',
        'end_day': '',
        'time': '2:45:43',
        'module': '1.3.1 Betriebs- und Kommunikationssysteme',
        'notes': 'Weitergearbeitet am Proj...',
        'long_notes': 'Weitergearbeitet am Projekt. Viel Fortschritt!'
      },
    ]
  }
  return render(request, 'dvmplanner/reports.html', data)

def review(request):
  data = {
    'uid': uid,
    'username': 'testuser',
  }
  return render(request, 'dvmplanner/review.html', data)

def admin(request):
  data = {
    'uid': uid,
    'username': 'testuser',
  }
  return render(request, 'dvmplanner/admin.html', data)

def profile(request):
  data = {
    'uid': uid,
    'username': 'testuser',
  }
  return render(request, 'dvmplanner/profile.html', data)

def addreport(request):
  data = {
    'uid': uid,
    'username': 'testuser',
  }
  return render(request, 'dvmplanner/addreport.html', data)