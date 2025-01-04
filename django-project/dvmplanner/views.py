from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles import finders
from dvmplanner.scripts.users import User
import os, json

uid = 'u0000'
if not finders.find(f'profiles/{uid}.png'):
  uid = '_default'

modules = [
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
            "name": "Einführung in die Informatik",
            "semester": "2"
          },
          {
            "index": "1.1.2",
            "name": "Vertiefung Informatik",
            "semester": "3"
          }
        ]
      },
      {
        "index": "1.2",
        "name": "E-Government mit Exkursionen",
        "submodules": [
          {
            "index": "1.2.1",
            "name": "E-Government mit Exkursionen",
            "semester": "1"
          }
        ]
      },
      {
        "index": "1.3",
        "name": "Betriebs- und Kommunikationssysteme/ verteilte Systeme",
        "submodules": [
          {
            "index": "1.3.1",
            "name": "Betriebs- und Kommunikationssysteme",
            "semester": "3"
          },
          {
            "index": "1.3.2",
            "name": "Verteilte Systeme",
            "semester": "4"
          },
          {
            "index": "1.3.3",
            "name": "Aktuelle Anwendungen erproben, Web Collagen, Roboter bauen, Raspberry Pi",
            "semester": "4"
          }
        ]
      },
      {
        "index": "1.4",
        "name": "Vorgehensmodelle der Softwareentwicklung, Requirements-Engineering und Requirements-Management",
        "submodules": [
          {
            "index": "1.4.1",
            "name": "Vorgehensmodelle (Software-Engineering 1)",
            "semester": "1"
          },
          {
            "index": "1.4.2",
            "name": "Requirements-Engineering und Requirements-Management (Software-Engineering 2)",
            "semester": "2"
          }
        ]
      },
      {
        "index": "1.5",
        "name": "Systemanalyse, Softwareentwurf und Implementierung, Softwarequilität und Test",
        "submodules": [
          {
            "index": "1.5.1",
            "name": "Systemanalyse (Software-Engineering 3)",
            "semester": "3"
          },
          {
            "index": "1.5.2",
            "name": "Softwareentwurf und Implementierung (Software-Engineering 4)",
            "semester": "4"
          },
          {
            "index": "1.5.3",
            "name": "Softwarequalität und Test (Software-Engineering 5)",
            "semester": "4"
          }
        ]
      },
      {
        "index": "1.6",
        "name": "Cybersecurity und ITIL",
        "submodules": [
          {
            "index": "1.6.1",
            "name": "Cybersecurity",
            "semester": "6"
          },
          {
            "index": "1.6.2",
            "name": "ITIL",
            "semester": "6"
          }
        ]
      },
      {
        "index": "1.7",
        "name": "IT-Management",
        "submodules": [
          {
            "index": "1.7.1",
            "name": "IT-Management",
            "semester": "5"
          }
        ]
      },
      {
        "index": "1.8",
        "name": "IT-Systeme und Informationssysteme",
        "submodules": [
          {
            "index": "1.8.1",
            "name": "IT-Systeme und Informationssysteme",
            "semester": "5"
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
            "index": "2.1.1",
            "name": "Steuerung, Public Management und Projektmanagement",
            "semester": "1"
          }
        ]
      },
      {
        "index": "2.2",
        "name": "Organisations- und Prozessmanagement",
        "submodules": [
          {
            "index": "2.2.1",
            "name": "Organisations- und Prozessmanagement",
            "semester": "3"
          }
        ]
      },
      {
        "index": "2.3",
        "name": "Öffentliche Betriebswirtschaftslehre",
        "submodules": [
          {
            "index": "2.3.1",
            "name": "Öffentliche Betriebswirtschaftslehre",
            "semester": "5"
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
            "name": "Grundlagen des Staats- und Europarechts",
            "semester": "1"
          },
          {
            "index": "3.1.2",
            "name": "Verwaltungsrecht",
            "semester": "1"
          }
        ]
      },
      {
        "index": "3.2",
        "name": "Kommunales Wirtschaftsrecht",
        "submodules": [
          {
            "index": "3.2.1",
            "name": "Kommunalrecht",
            "semester": "3"
          },
          {
            "index": "3.2.2",
            "name": "Finanzwirtschaft der Kommunen",
            "semester": "3"
          },
          {
            "index": "3.2.3",
            "name": "Staatliches Haushaltsrecht",
            "semester": "3"
          }
        ]
      },
      {
        "index": "3.3",
        "name": "Zivilrechtliche Grundlagen des Verwaltungshandelns",
        "submodules": [
          {
            "index": "3.3.1",
            "name": "Grundlagen des Zivilrechts",
            "semester": "2"
          },
          {
            "index": "3.3.2",
            "name": "Grundlagen des Kartell- und Wettbewerbsrechts",
            "semester": "2"
          },
          {
            "index": "3.3.3",
            "name": "Grundlagen des Handels- und Gesellschaftsrechts",
            "semester": "2"
          },
          {
            "index": "3.3.4",
            "name": "IT-Recht",
            "semester": "2"
          }
        ]
      },
      {
        "index": "3.4",
        "name": "Rechtliche Grundlagen der öffentlichen Beschaffung",
        "submodules": [
          {
            "index": "3.4.1",
            "name": "Vergaberecht (einschließlich E-Government)",
            "semester": "4"
          },
          {
            "index": "3.4.2",
            "name": "Beihilferecht",
            "semester": "4"
          }
        ]
      },
      {
        "index": "3.5",
        "name": "Rechtliche Grundlagen des Datenschutzes, Informationszugangsrecht und Personalrecht",
        "submodules": [
          {
            "index": "3.5.1",
            "name": "Recht Datenschutzes",
            "semester": "5"
          },
          {
            "index": "3.5.2",
            "name": "Informationszugangsrecht",
            "semester": "5"
          },
          {
            "index": "3.5.3",
            "name": "Arbeitsrecht",
            "semester": "5"
          },
          {
            "index": "3.5.4",
            "name": "Beamtenrecht",
            "semester": "5"
          }
        ]
      },
      {
        "index": "3.6",
        "name": "Vertragsgestaltung und rechtliche Kernkompetenzen",
        "submodules": [
          {
            "index": "3.6.1",
            "name": "Vertragsgestaltung",
            "semester": "6"
          },
          {
            "index": "3.6.2",
            "name": "Rechtliche Kernkompetenzen bei Digitalisierungsprojekten",
            "semester": "6"
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
            "name": "Strategische und integrale Steuerung",
            "semester": "1"
          },
          {
            "index": "4.1.2",
            "name": "Smart Cities und Smart Services",
            "semester": "1"
          },
          {
            "index": "4.1.3",
            "name": "Grundlagen des Change Managements",
            "semester": "2"
          }
        ]
      },
      {
        "index": "4.2",
        "name": "Führung, Kommunikation und Partizipation im digitalen Kontext",
        "submodules": [
          {
            "index": "4.2.1",
            "name": "Gestaltung von Kommunikation und Partizipation mit digitalen Medien",
            "semester": "4"
          },
          {
            "index": "4.2.2",
            "name": "Führung und Teamentwicklung mit digitalen Medien",
            "semester": "3"
          },
          {
            "index": "4.2.3",
            "name": "Digitalisierung und digitales Wissensmanagement",
            "semester": "4"
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
            "index": "5.1.1",
            "name": "Praktikum 1",
            "semester": "1"
          }
        ]
      },
      {
        "index": "5.2",
        "name": "Praktikum 7",
        "submodules": [
          {
            "index": "5.2.1",
            "name": "Praktikum 7",
            "semester": "6"
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
            "index": "6.1.1",
            "name": "Fallstudie 1",
            "semester": "2"
          }
        ]
      },
      {
        "index": "6.2",
        "name": "Fallstudie 2",
        "submodules": [
          {
            "index": "6.2.1",
            "name": "Fallstudie 2",
            "semester": "3"
          }
        ]
      },
      {
        "index": "6.3",
        "name": "Fallstudie 3",
        "submodules": [
          {
            "index": "6.3.1",
            "name": "Fallstudie 3",
            "semester": "4"
          }
        ]
      },
      {
        "index": "6.4",
        "name": "Fallstudie 4",
        "submodules": [
          {
            "index": "6.4.1",
            "name": "Fallstudie 4",
            "semester": "5"
          }
        ]
      },
      {
        "index": "6.5",
        "name": "Fallstudie 5",
        "submodules": [
          {
            "index": "6.5.1",
            "name": "Fallstudie 5",
            "semester": "6"
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
        "index": "7.1",
        "name": "Bachelorarbeit",
        "submodules": [
          {
            "index": "7.1.1",
            "name": "Bachelorarbeit",
            "semester": "6"
          }
        ]
      }
    ]
  }
]

def home(request):
  # redirect if logged in
  data = {}
  return render(request, 'dvmplanner/home.html', data)

def dashboard(request):
  # usernames = []
  # users = User.getUsers()
  # for user in users:
  #   usernames.append(user.getUsername())
  # data = {
  #   'usernames': usernames
  # }
  data = {
    'active_page': 'dashboard',
    'uid': uid,
    'username': 'testuser',
    'first_name': 'Max',
    'last_name': 'Mustermann',
    'role': 'admin',
    'img': True,
    'current_activity': {
      'status': 'active', # active, paused, finished, none
      'day': '02.01.2025',
      'start': '14.34:23 Uhr',
      'entries': [
        {
          'day': '02.01.2025',
          'start': '14.34:23 Uhr',
          'end_day': '02.01.2025',
          'end': '15.53:40 Uhr',
          'time': '2:19:17'
        },
        {
          'day': '02.01.2025',
          'start': '14.34:23 Uhr',
          'end_day': '02.01.2025',
          'end': '15.53:40 Uhr',
          'time': '2:19:17'
        }
      ]
    },
    'placeholder_module': {
      'name': 'Einführung in die Informatik',
      'index': '1.1.1'
    },
    'modules': modules
  }
  return render(request, 'dvmplanner/dashboard.html', data)

def reports(request):
  '''
  Important Notes:
  - Wenn Endzeit ein neuer Tag ist -> 'end_day' befüllen, ansonsten leer lassen
  - Wenn Notizen länger als Anzahl Buchstaben -> verkürzte version in 'notes' und lange in 'long_notes', ansonsten 'long_notes' leer lassen
  '''
  data = {
    'active_page': 'reports',
    'uid': uid,
    'username': 'testuser',
    'first_name': 'Max',
    'last_name': 'Mustermann',
    'role': 'admin',
    'img': True,
    'current_module': '[Alle]',
    'current_semester': '[Alle]',
    'modules': modules,
    'reports': [
      {
        'id': 'r0001',
        'day': '21.11.2024',
        'start': '10.12:43 Uhr',
        'end': '12.58:26 Uhr',
        'end_day': '',
        'time': '2:45:43',
        'module_index': '1.3.1',
        'module_name': 'Betriebs- und Kommunikationssysteme',
        'notes': 'Weitergearbeitet am Proj...',
        'long_notes': 'Weitergearbeitet am Projekt. Viel Fortschritt!'
      },
      {
        'id': 'r0002',
        'day': '21.11.2024',
        'start': '10.12:43 Uhr',
        'end': '12.58:26 Uhr',
        'end_day': '22.11.2024',
        'time': '2:45:43',
        'module_index': '1.3.1',
        'module_name': 'Betriebs- und Kommunikationssysteme',
        'notes': 'Weitergearbeitet am Projekt',
        'long_notes': ''
      },
      {
        'id': 'r0003',
        'day': '21.11.2024',
        'start': '10.12:43 Uhr',
        'end': '12.58:26 Uhr',
        'end_day': '',
        'time': '2:45:43',
        'module_index': '1.3.1',
        'module_name': 'Betriebs- und Kommunikationssysteme',
        'notes': 'Weitergearbeitet am Proj...',
        'long_notes': 'Weitergearbeitet am Projekt. Viel Fortschritt!'
      },
    ]
  }
  return render(request, 'dvmplanner/reports.html', data)

def review(request):
  review_data = [
    {
      'module': '1.1.2 Vertiefung Informatik',
      'time': '12:45:43',
      'sessions': '14'
    },
    {
      'module': '1.5.1 Systemanalyse (Software-Engineering 3)',
      'time': '23:34:02',
      'sessions': '18'
    },
    {
      'module': '2.1.1 Steuerung, Public Management und Projektmanagement',
      'time': '4:12:52',
      'sessions': '3'
    },
    {
      'module': '3.3.4 IT-Recht',
      'time': '7:40:29',
      'sessions': '5'
    },
  ]
  data = {
    'active_page': 'review',
    'uid': uid,
    'username': 'testuser',
    'first_name': 'Max',
    'last_name': 'Mustermann',
    'role': 'admin',
    'img': True,
    'current_module': '[Alle]',
    'current_semester': '[Alle]',
    'modules': modules,
    'total_time': '48:13:06',
    'total_sessions': '40',
    'reviews': [
      {
        'module': '1.1.2 Vertiefung Informatik',
        'semester': '3',
        'time': '12:45:43',
        'percentage': '26,57 %',
        'sessions': '14'
      },
      {
        'module': '1.5.1 Systemanalyse (Software-Engineering 3)',
        'semester': '3',
        'time': '23:34:02',
        'percentage': '48,88 %',
        'sessions': '18'
      },
      {
        'module': '2.1.1 Steuerung, Public Management und Projektmanagement',
        'semester': '1',
        'time': '4:12:52',
        'percentage': '8,74 %',
        'sessions': '3'
      },
      {
        'module': '3.3.4 IT-Recht',
        'semester': '2',
        'time': '7:40:29',
        'percentage': '15,92 %',
        'sessions': '5'
      },
    ],
    'review_data': json.dumps(review_data)
  }
  return render(request, 'dvmplanner/review.html', data)

def admin(request):
  data = {
    'active_page': 'admin',
    'uid': uid,
    'username': 'testuser',
    'first_name': 'Max',
    'last_name': 'Mustermann',
    'role': 'admin',
    'img': True,
    'current_requests_filter_role': '[Alle]',
    'requests': [
      {
        'day': '15.12.2024',
        'time': '10.12:43 Uhr',
        'first_name': 'Julius',
        'last_name': 'Cäsar',
        'username': 'thedestroyer123',
        'role': 'vip',
        'requested_role': 'admin',
      },
      {
        'day': '13.12.2024',
        'time': '15.12:43 Uhr',
        'first_name': 'Leonardo',
        'last_name': 'da Vinci',
        'username': 'the_real_vinci',
        'role': 'normal',
        'requested_role': 'vip',
      },
      {
        'day': '12.12.2024',
        'time': '13.12:43 Uhr',
        'first_name': 'Marie',
        'last_name': 'Curie',
        'username': 'radium',
        'role': 'vip',
        'requested_role': 'admin',
      },
    ],
    'current_users_filter_role': '[Alle]',
    'current_users_filter_status': '[Alle]',
    'users': [
      {
        'day': '15.12.2024',
        'time': '10.12:43 Uhr',
        'first_name': 'Julius',
        'last_name': 'Cäsar',
        'username': 'thedestroyer123',
        'role': 'vip',
        'status': 'active',
        'id': 'u0001'
      },
      {
        'day': '13.12.2024',
        'time': '15.12:43 Uhr',
        'first_name': 'Leonardo',
        'last_name': 'da Vinci',
        'username': 'the_real_vinci',
        'role': 'normal',
        'status': 'deleted',
        'id': 'u0002'
      },
      {
        'day': '12.12.2024',
        'time': '13.12:43 Uhr',
        'first_name': 'Marie',
        'last_name': 'Curie',
        'username': 'radium',
        'role': 'admin',
        'status': 'blocked',
        'id': 'u0003'
      }
    ],
    'modules': modules
  }
  return render(request, 'dvmplanner/admin.html', data)

def profile(request):
  data = {
    'active_page': 'profile',
    'uid': uid,
    'username': 'testuser',
    'first_name': 'Max',
    'last_name': 'Mustermann',
    'role': 'vip',
    'img': True,
    'email': 'Mustermann_Max@teams.hs-ludwigsburg.de',
    'pwd': '123',
    'creation_date': '28.12.2024, 13.48:11 Uhr',
    'requested_role': ''
  }
  return render(request, 'dvmplanner/profile.html', data)

def addreport(request):
  data = {
    'active_page': 'addreport',
    'uid': uid,
    'username': 'testuser',
    'first_name': 'Max',
    'last_name': 'Mustermann',
    'role': 'admin',
    'img': True,
    'placeholder_module': {
      'name': 'Einführung in die Informatik',
      'index': '1.1.1'
    },
    'modules': modules
  }
  return render(request, 'dvmplanner/addreport.html', data)

def login(request):
  data = {}
  return render(request, 'dvmplanner/login.html', data)

def signup(request):
  data = {}
  return render(request, 'dvmplanner/signup.html', data)