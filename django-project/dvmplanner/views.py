from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles import finders
from dvmplanner.scripts.users import User
from dvmplanner.scripts.modules import Submodule
from dvmplanner.scripts.main import BASE_DIR, formatTimedelta
from datetime import datetime, timedelta
import os, json

def home(request):
  if 'uid' in request.session:
    return redirect(dashboard)
  else:
    data = {}
    return render(request, 'dvmplanner/home.html', data)

def dashboard(request):
  if 'uid' in request.session:
    user = User.getUserByKey('uid', request.session.get('uid'))

    lastReports = []
    latestReports = sorted(user.getData('reports'), key = lambda x: x.getData('start'), reverse = True)[:5]
    for report in latestReports:
      lastReports.append(report.getFormattedData())

    totalTime = timedelta(0)
    totalSessions = 0
    reviewDataRaw = {}
    for report in user.getData('reports'):
      totalTime += report.getData('end') - report.getData('start')
      totalSessions += 1
      moduleIndex = report.getData('submodule').getCompleteIndex()
      if moduleIndex not in reviewDataRaw:
        reviewDataRaw[moduleIndex] = {
          'time': timedelta(0),
          'sessions': 0
        }
      reviewDataRaw[moduleIndex]['time'] += report.getData('end') - report.getData('start')
      reviewDataRaw[moduleIndex]['sessions'] += 1
    totalTime = formatTimedelta(totalTime)

    reviewData = []
    reviewDataRaw = { key: reviewDataRaw[key] for key in sorted(reviewDataRaw) }
    for module in reviewDataRaw:
      reviewData.append({
        'module': f'{ module } { Submodule.getByIndex(module).getData('name') }',
        'time': formatTimedelta(reviewDataRaw[module]['time']),
        'sessions': reviewDataRaw[module]['sessions']
      })    

    modules = Submodule.getAllFormattedModules()

    data = {
      'active_page': 'dashboard',
      'uid': user.getData('uid'),
      'username': user.getData('username'),
      'first_name': user.getData('first_name'),
      'last_name': user.getData('last_name'),
      'role': user.getData('role'),
      'img': user.getData('img'),
      'current_activity': user.getData('current_activity'),
      'placeholder_module': {
        'name': modules[0]['modules'][0]['submodules'][0]['name'],
        'index': modules[0]['modules'][0]['submodules'][0]['index']
      },
      'modules': modules,
      'last_reports': lastReports,
      'total_time': totalTime,
      'total_sessions': totalSessions,
      'review_data': json.dumps(reviewData),
      'requests': User.getFormattedRequests(),
      'requested_role': user.getData('requested_role')
    }

    if 'notification' in request.session:
      data['notification'] = request.session.get('notification')
      del request.session['notification']

    return render(request, 'dvmplanner/dashboard.html', data)
  
  else:
    return redirect(home)

def reports(request):
  '''
  Important Notes:
  - Wenn Endzeit ein neuer Tag ist -> 'end_day' befüllen, ansonsten leer lassen
  - Wenn Notizen länger als Anzahl Buchstaben -> verkürzte version in 'notes' und lange in 'long_notes', ansonsten 'long_notes' leer lassen
  '''
  data = {
    'active_page': 'reports',
    'uid': 'u0000',
    'username': 'testuser',
    'first_name': 'Max',
    'last_name': 'Mustermann',
    'role': 'admin',
    'img': True,
    'current_module': '[Alle]',
    'current_semester': '[Alle]',
    'modules': Submodule.getAllFormattedModules(),
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

  if 'uid' in request.session:
    return render(request, 'dvmplanner/reports.html', data)
  else:
    return redirect(home)

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
    'uid': 'u0000',
    'username': 'testuser',
    'first_name': 'Max',
    'last_name': 'Mustermann',
    'role': 'admin',
    'img': True,
    'current_module': '[Alle]',
    'current_semester': '[Alle]',
    'modules': Submodule.getAllFormattedModules(),
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

  if 'uid' in request.session:
    return render(request, 'dvmplanner/review.html', data)
  else:
    return redirect(home)

def admin(request):
  data = {
    'active_page': 'admin',
    'uid': 'u0000',
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
        'id': 'u0001'
      },
      {
        'day': '13.12.2024',
        'time': '15.12:43 Uhr',
        'first_name': 'Leonardo',
        'last_name': 'da Vinci',
        'username': 'the_real_vinci',
        'role': 'normal',
        'requested_role': 'vip',
        'id': 'u0002'
      },
      {
        'day': '12.12.2024',
        'time': '13.12:43 Uhr',
        'first_name': 'Marie',
        'last_name': 'Curie',
        'username': 'radium',
        'role': 'vip',
        'requested_role': 'admin',
        'id': 'u0003'
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
    'modules': Submodule.getAllFormattedModules()
  }

  if 'uid' in request.session:
    return render(request, 'dvmplanner/admin.html', data)
  else:
    return redirect(home)

def profile(request):
  data = {
    'active_page': 'profile',
    'uid': 'u0000',
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

  if 'uid' in request.session:
    return render(request, 'dvmplanner/profile.html', data)
  else:
    return redirect(home)

def addreport(request):
  data = {
    'active_page': 'addreport',
    'uid': 'u0000',
    'username': 'testuser',
    'first_name': 'Max',
    'last_name': 'Mustermann',
    'role': 'admin',
    'img': True,
    'placeholder_module': {
      'name': 'Einführung in die Informatik',
      'index': '1.1.1'
    },
    'modules': Submodule.getAllFormattedModules()
  }

  if 'uid' in request.session:
    return render(request, 'dvmplanner/addreport.html', data)
  else:
    return redirect(home)

def login(request):
  if request.POST.get('context', '') == 'login':
    username = request.POST.get('username', '')
    pwd = request.POST.get('pwd', '')
    user = User.getUserByKey('username', username)
    if user is None:
      user = User.getUserByKey('email', username)
    if user is not None:
      if user.checkPwd(pwd):
        request.session['uid'] = user.getData('uid')
        request.session['notification'] = f'Erfolgreich als { user.getData('username') } angemeldet.'
        return redirect(dashboard)
      else:
        data = {
          'notification': 'Falsches Passwort!'
        }
        return render(request, 'dvmplanner/login.html', data)
    else:
      data = {
        'notification': 'Falscher Benutzername oder E-Mail!'
      }
      return render(request, 'dvmplanner/login.html', data)
  else:
    return render(request, 'dvmplanner/login.html')

def signup(request):
  if request.POST.get('context', '') == 'signup':
    username = request.POST.get('username', '')
    firstName = request.POST.get('first_name', '')
    lastName = request.POST.get('last_name', '')
    email = request.POST.get('email', '')
    pwd = request.POST.get('pwd', '')
    pwdRepeat = request.POST.get('pwd_repeat', '')
    if User.getUserByKey('email', email):
      data = {
        'notification': 'Die E-Mail ist bereits vergeben!'
      }
      return render(request, 'dvmplanner/signup.html', data)
    elif User.getUserByKey('username', username):
      data = {
        'notification': 'Der Benutzername ist bereits vergeben!'
      }
      return render(request, 'dvmplanner/signup.html', data)
    elif pwd != pwdRepeat:
      data = {
        'notification': 'Die Passwörter stimmen nicht überein!'
      }
      return render(request, 'dvmplanner/signup.html', data)
    else:
      user = User.createUser(username, firstName, lastName, email, pwd)
      request.session['uid'] = user.getData('uid')
      request.session['notification'] = f'Der Benutzer { username } wurde angelegt.'
      return redirect(dashboard)
  else:
    return render(request, 'dvmplanner/signup.html')