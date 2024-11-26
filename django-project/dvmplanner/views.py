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
    'modules': {
      '1 Technische Dimensionen der Digitalisierung': {
        '1.1 Informatik Einführung und Vertiefung': [
          '1.1.2 Einführung in die Informatik',
          '1.1.3 Vertiefung Informatik'
        ],
        '1.2 E-Government mit Exkursionen': [
          '1.2.0 E-Government mit Exkursionen'
        ],
        '1.3 Betriebs- und Kommunikationssysteme/ verteilte Systeme': [
          '1.3.1 Betriebs- und Kommunikationssysteme',
          '1.3.2 Verteilte Systeme',
          '1.3.3 Aktuelle Anwendungen erproben, Web Collagen, Roboter bauen, Raspberry Pi'
        ],
        '1.4 Vorgehensmodelle der Softwareentwicklung, Requirements-Engineering und Requirements-Management': [
          '1.4.1 Vorgehensmodelle (Software-Engineering 1)',
          '1.4.2 Requirements-Engineering und Requirements-Management (Software-Engineering 2)'
        ],
        '1.5 Systemanalyse, Softwareentwurf und Implementierung, Softwarequilität und Test': [
          '1.5.1 Systemanalyse (Software-Engineering 3)',
          '1.5.2 Softwareentwurf und Implementierung (Software-Engineering 4)',
          '1.5.3 Softwarequalität und Test (Software-Engineering 5)'
        ],
        '1.6 Cybersecurity und ITIL': [
          '1.6.1 Cybersecurity',
          '1.6.2 ITIL'
        ],
        '1.7 IT-Management': [
          '1.7.0 IT-Management'
        ],
        '1.8 IT-Systeme und Informationssysteme': [
          '1.8.0 IT-Systeme und Informationssysteme'
        ]
      },
      '2 Verwaltungsmanagement': {
        '2.1 Steuerung, Public Management und Projektmanagement': [
          '2.1.0 Steuerung, Public Management und Projektmanagement'
        ],
        '2.2 Organisations- und Prozessmanagement': [
          '2.2.0 Organisations- und Prozessmanagement'
        ],
        '2.3 Öffentliche Betriebswirtschaftslehre': [
          '2.3.0 Öffentliche Betriebswirtschaftslehre'
        ]
      },
      '3 Rechtliche Grundlagen der öffentlichen Verwaltung': {
        '3.1 Öffentlich-rechtliche Grundlagen der Verwaltungsorganisation und des Verwaltungshandelns': [
          '3.1.1 Grundlagen des Staats- und Europarechts',
          '3.1.2 Verwaltungsrecht'
        ],
        '3.2 Kommunales Wirtschaftsrecht': [
          '3.2.1 Kommunalrecht',
          '3.2.2 Finanzwirtschaft der Kommunen',
          '3.2.3 Staatliches Haushaltsrecht'
        ],
        '3.3 Zivilrechtliche Grundlagen des Verwaltungshandelns': [
          '3.3.1 Grundlagen des Zivilrechts',
          '3.3.2 Grundlagen des Kartell- und Wettbewerbsrechts',
          '3.3.3 Grundlagen des Handels- und Gesellschaftsrechts',
          '3.3.4 IT-Recht'
        ],
        '3.4 Rechtliche Grundlagen der öffentlichen Beschaffung': [
          '3.4.1 Vergaberecht (einschließlich E-Government)',
          '3.4.2 Beihilferecht'
        ],
        '3.5 Rechtliche Grundlagen des Datenschutzes, Informationszugangsrecht und Personalrecht': [
          '3.5.1 Recht Datenschutzes',
          '3.5.2 Informationszugangsrecht',
          '3.5.3 Arbeitsrecht',
          '3.5.4 Beamtenrecht'
        ],
        '3.6 Vertragsgestaltung und rechtliche Kernkompetenzen': [
          '3.6.1 Vertragsgestaltung',
          '3.6.2 Rechtliche Kernkompetenzen bei Digitalisierungsprojekten'
        ]
      },
      '4 Digital Leadership': {
        '4.1 Digital Governance: Von der ganzheitlichen Strategie zur Umsetzung': [
          '4.1.1 Strategische und integrale Steuerung',
          '4.1.2 Smart Cities und Smart Services',
          '4.1.3 Grundlagen des Change Managements'
        ],
        '4.2 Führung, Kommunikation und Partizipation im digitalen Kontext': [
          '4.2.1 Gestaltung von Kommunikation und Partizipation mit digitalen Medien',
          '4.2.2 Führung und Teamentwicklung mit digitalen Medien',
          '4.2.3 Digitalisierung und digitales Wissensmanagement'
        ]
      },
      '5 Praxisphasen Praktika 1 und 7': {
        '5.1 Praktikum 1': [
          '5.1.0 Praktikum 1'
        ],
        '5.2 Praktikum 7': [
          '5.2.0 Praktikum 7'
        ]
      },
      '6 Fallstudien': {
        '6.1 Fallstudie 1': [
          '6.1.0 Fallstudie 1'
        ],
        '6.2 Fallstudie 2': [
          '6.2.0 Fallstudie 2'
        ],
        '6.3 Fallstudie 3': [
          '6.3.0 Fallstudie 3'
        ],
        '6.4 Fallstudie 4': [
          '6.4.0 Fallstudie 4'
        ],
        '6.5 Fallstudie 5': [
          '6.5.0 Fallstudie 5'
        ]
      },
      '7 Bachelorarbeit': {
        '7.0 Bachelorarbeit': [
          '7.0.0 Bachelorarbeit'
        ]
      }
    },
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