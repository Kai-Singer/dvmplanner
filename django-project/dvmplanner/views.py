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
    'first_name': 'Max',
    'last_name': 'Mustermann',
    'role': 'admin',
    'current_module': '[Alle]',
    'modules': [
      {
        "index": "1",
        "name": "Technische Dimensionen der Digitalisierung",
        "modules": [
          {
            "index": "1.1",
            "name": "Informatik Einführung und Vertiefung",
            "submodules": [
              {
                "index": "1.1.1",
                "name": "Einführung in die Informatik"
              },
              {
                "index": "1.1.2",
                "name": "Vertiefung Informatik"
              }
            ]
          },
          {
            "index": "1.2",
            "name": "E-Government mit Exkursionen",
            "submodules": [
              {
                "index": "1.2.0",
                "name": "E-Government mit Exkursionen"
              }
            ]
          },
          {
            "index": "1.3",
            "name": "Betriebs- und Kommunikationssysteme/ verteilte Systeme",
            "submodules": [
              {
                "index": "1.3.1",
                "name": "Betriebs- und Kommunikationssysteme"
              },
              {
                "index": "1.3.2",
                "name": "Verteilte Systeme"
              },
              {
                "index": "1.3.3",
                "name": "Aktuelle Anwendungen erproben, Web Collagen, Roboter bauen, Raspberry Pi"
              }
            ]
          },
          {
            "index": "1.4",
            "name": "Vorgehensmodelle der Softwareentwicklung, Requirements-Engineering und Requirements-Management",
            "submodules": [
              {
                "index": "1.4.1",
                "name": "Vorgehensmodelle (Software-Engineering 1)"
              },
              {
                "index": "1.4.2",
                "name": "Requirements-Engineering und Requirements-Management (Software-Engineering 2)"
              }
            ]
          },
          {
            "index": "1.5",
            "name": "Systemanalyse, Softwareentwurf und Implementierung, Softwarequilität und Test",
            "submodules": [
              {
                "index": "1.5.1",
                "name": "Systemanalyse (Software-Engineering 3)"
              },
              {
                "index": "1.5.2",
                "name": "Softwareentwurf und Implementierung (Software-Engineering 4)"
              },
              {
                "index": "1.5.3",
                "name": "Softwarequalität und Test (Software-Engineering 5)"
              }
            ]
          },
          {
            "index": "1.6",
            "name": "Cybersecurity und ITIL",
            "submodules": [
              {
                "index": "1.6.1",
                "name": "Cybersecurity"
              },
              {
                "index": "1.6.2",
                "name": "ITIL"
              }
            ]
          },
          {
            "index": "1.7",
            "name": "IT-Management",
            "submodules": [
              {
                "index": "1.7.0",
                "name": "IT-Management"
              }
            ]
          },
          {
            "index": "1.8",
            "name": "IT-Systeme und Informationssysteme",
            "submodules": [
              {
                "index": "1.8.0",
                "name": "IT-Systeme und Informationssysteme"
              }
            ]
          }
        ]
      },
      {
        "index": "2",
        "name": "Verwaltungsmanagement",
        "modules": [
          {
            "index": "2.1",
            "name": "Steuerung, Public Management und Projektmanagement",
            "submodules": [
              {
                "index": "2.1.0",
                "name": "Steuerung, Public Management und Projektmanagement"
              }
            ]
          },
          {
            "index": "2.2",
            "name": "Organisations- und Prozessmanagement",
            "submodules": [
              {
                "index": "2.2.0",
                "name": "Organisations- und Prozessmanagement"
              }
            ]
          },
          {
            "index": "2.3",
            "name": "Öffentliche Betriebswirtschaftslehre",
            "submodules": [
              {
                "index": "2.3.0",
                "name": "Öffentliche Betriebswirtschaftslehre"
              }
            ]
          }
        ]
      },
      {
        "index": "3",
        "name": "Rechtliche Grundlagen der öffentlichen Verwaltung",
        "modules": [
          {
            "index": "3.1",
            "name": "Öffentlich-rechtliche Grundlagen der Verwaltungsorganisation und des Verwaltungshandelns",
            "submodules": [
              {
                "index": "3.1.1",
                "name": "Grundlagen des Staats- und Europarechts"
              },
              {
                "index": "3.1.2",
                "name": "Verwaltungsrecht"
              }
            ]
          },
          {
            "index": "3.2",
            "name": "Kommunales Wirtschaftsrecht",
            "submodules": [
              {
                "index": "3.2.1",
                "name": "Kommunalrecht"
              },
              {
                "index": "3.2.2",
                "name": "Finanzwirtschaft der Kommunen"
              },
              {
                "index": "3.2.3",
                "name": "Staatliches Haushaltsrecht"
              }
            ]
          },
          {
            "index": "3.3",
            "name": "Zivilrechtliche Grundlagen des Verwaltungshandelns",
            "submodules": [
              {
                "index": "3.3.1",
                "name": "Grundlagen des Zivilrechts"
              },
              {
                "index": "3.3.2",
                "name": "Grundlagen des Kartell- und Wettbewerbsrechts"
              },
              {
                "index": "3.3.3",
                "name": "Grundlagen des Handels- und Gesellschaftsrechts"
              },
              {
                "index": "3.3.4",
                "name": "IT-Recht"
              }
            ]
          },
          {
            "index": "3.4",
            "name": "Rechtliche Grundlagen der öffentlichen Beschaffung",
            "submodules": [
              {
                "index": "3.4.1",
                "name": "Vergaberecht (einschließlich E-Government)"
              },
              {
                "index": "3.4.2",
                "name": "Beihilferecht"
              }
            ]
          },
          {
            "index": "3.5",
            "name": "Rechtliche Grundlagen des Datenschutzes, Informationszugangsrecht und Personalrecht",
            "submodules": [
              {
                "index": "3.5.1",
                "name": "Recht Datenschutzes"
              },
              {
                "index": "3.5.2",
                "name": "Informationszugangsrecht"
              },
              {
                "index": "3.5.3",
                "name": "Arbeitsrecht"
              },
              {
                "index": "3.5.4",
                "name": "Beamtenrecht"
              }
            ]
          },
          {
            "index": "3.6",
            "name": "Vertragsgestaltung und rechtliche Kernkompetenzen",
            "submodules": [
              {
                "index": "3.6.1",
                "name": "Vertragsgestaltung"
              },
              {
                "index": "3.6.2",
                "name": "Rechtliche Kernkompetenzen bei Digitalisierungsprojekten"
              }
            ]
          }
        ]
      },
      {
        "index": "4",
        "name": "Digital Leadership",
        "modules": [
          {
            "index": "4.1",
            "name": "Digital Governance: Von der ganzheitlichen Strategie zur Umsetzung",
            "submodules": [
              {
                "index": "4.1.1",
                "name": "Strategische und integrale Steuerung"
              },
              {
                "index": "4.1.2",
                "name": "Smart Cities und Smart Services"
              },
              {
                "index": "4.1.3",
                "name": "Grundlagen des Change Managements"
              }
            ]
          },
          {
            "index": "4.2",
            "name": "Führung, Kommunikation und Partizipation im digitalen Kontext",
            "submodules": [
              {
                "index": "4.2.1",
                "name": "Gestaltung von Kommunikation und Partizipation mit digitalen Medien"
              },
              {
                "index": "4.2.2",
                "name": "Führung und Teamentwicklung mit digitalen Medien"
              },
              {
                "index": "4.2.3",
                "name": "Digitalisierung und digitales Wissensmanagement"
              }
            ]
          }
        ]
      },
      {
        "index": "5",
        "name": "Praxisphasen Praktika 1 und 7",
        "modules": [
          {
            "index": "5.1",
            "name": "Praktikum 1",
            "submodules": [
              {
                "index": "5.1.0",
                "name": "Praktikum 1"
              }
            ]
          },
          {
            "index": "5.2",
            "name": "Praktikum 7",
            "submodules": [
              {
                "index": "5.2.0",
                "name": "Praktikum 7"
              }
            ]
          }
        ]
      },
      {
        "index": "6",
        "name": "Fallstudien",
        "modules": [
          {
            "index": "6.1",
            "name": "Fallstudie 1",
            "submodules": [
              {
                "index": "6.1.0",
                "name": "Fallstudie 1"
              }
            ]
          },
          {
            "index": "6.2",
            "name": "Fallstudie 2",
            "submodules": [
              {
                "index": "6.2.0",
                "name": "Fallstudie 2"
              }
            ]
          },
          {
            "index": "6.3",
            "name": "Fallstudie 3",
            "submodules": [
              {
                "index": "6.3.0",
                "name": "Fallstudie 3"
              }
            ]
          },
          {
            "index": "6.4",
            "name": "Fallstudie 4",
            "submodules": [
              {
                "index": "6.4.0",
                "name": "Fallstudie 4"
              }
            ]
          },
          {
            "index": "6.5",
            "name": "Fallstudie 5",
            "submodules": [
              {
                "index": "6.5.0",
                "name": "Fallstudie 5"
              }
            ]
          }
        ]
      },
      {
        "index": "7",
        "name": "Bachelorarbeit",
        "modules": [
          {
            "index": "7.0",
            "name": "Bachelorarbeit",
            "submodules": [
              {
                "index": "7.0.0",
                "name": "Bachelorarbeit"
              }
            ]
          }
        ]
      }
    ],
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
    'first_name': 'Max',
    'last_name': 'Mustermann'
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