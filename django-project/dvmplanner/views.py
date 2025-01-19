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
    if 'notification' in request.session:
      data['notification'] = request.session['notification']
      del request.session['notification']

    return render(request, 'dvmplanner/home.html', data)

def dashboard(request):
  if 'uid' in request.session:
    user = User.getUserByKey('uid', request.session['uid'])

    if request.POST.get('context', '') == 'start_report':
      if 'current_activity' in request.session:
        del request.session['current_activity']
      request.session['current_activity'] = { 
        'status': 'active',
        'entries': [
          {
            'start': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'end': ''
          }
        ]
      }

    elif request.POST.get('context', '') == 'pause_report':
      currentActivitySession = request.session['current_activity']
      currentActivitySession['status'] = 'paused'
      currentActivitySession['entries'][-1]['end'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      request.session['current_activity'] = currentActivitySession
      
    elif request.POST.get('context', '') == 'resume_report':
      currentActivitySession = request.session['current_activity']
      currentActivitySession['status'] = 'active'
      currentActivitySession['entries'].append({
        'start': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'end': ''
      })
      request.session['current_activity'] = currentActivitySession

    elif request.POST.get('context', '') == 'finish_report':
      currentActivitySession = request.session['current_activity']
      if currentActivitySession['status'] == 'active':
        currentActivitySession['entries'][-1]['end'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      currentActivitySession['status'] = 'finished'
      request.session['current_activity'] = currentActivitySession

    elif request.POST.get('context', '') == 'checkin_report':
      entries = request.session['current_activity']['entries']
      missingEnd = False
      for entry in entries:
        if entry['end'] == '':
          missingEnd = True
      if len(entries) <= 0:
        request.session['notification'] = 'Du kannst einen Arbeitsbericht ohne aufgezeichnete Zeiten nicht abspeichern!'
      elif missingEnd:
        request.session['notification'] = 'Beende zuerst alle Zeiten bevor du den Arbeitsbericht abspeichern kannst!'
      else:
        moduleIndex = request.POST.get('module', '1.1.1')
        module = Submodule.getByIndex(moduleIndex)
        notes = request.POST.get('notes', '')
        for entry in entries:
          start = datetime.strptime(entry['start'], '%Y-%m-%d %H:%M:%S')
          end = datetime.strptime(entry['end'], '%Y-%m-%d %H:%M:%S')
          user.addReport(start, end, module, notes)
        del request.session['current_activity']

    elif request.POST.get('context', '') == 'delete_entries':
      del request.session['current_activity']

    elif request.POST.get('context', '') == 'delete_entry':
      entryIndex = request.POST.get('index', 0)
      currentActivitySession = request.session['current_activity']
      del currentActivitySession['entries'][int(entryIndex)]
      request.session['current_activity'] = currentActivitySession

    lastReports = []
    latestReports = sorted(user.getData('reports'), key = lambda x: x.getData('start'), reverse = True)[:5]
    for report in latestReports:
      lastReports.append(report.getFormattedData())   

    modules = Submodule.getAllFormattedModules()
    reviewData = user.getFormattedReview()

    currentActivity = {}
    if 'current_activity' in request.session:
      currentActivitySession = request.session['current_activity']
      currentActivity['status'] = currentActivitySession['status']
      currentActivity['entries'] = []
      for entry in currentActivitySession['entries']:
        start = datetime.strptime(entry['start'], '%Y-%m-%d %H:%M:%S')
        currentActivityEntry = {
          'day': start.strftime('%d.%m.%Y'),
          'start': start.strftime('%H.%M:%S Uhr'),
          'end_day': '',
          'end': '',
          'time': ''
        }
        if entry['end'] != '':
          end = datetime.strptime(entry['end'], '%Y-%m-%d %H:%M:%S')
          currentActivityEntry['end_day'] = end.strftime('%d.%m.%Y')
          currentActivityEntry['end'] = end.strftime('%H.%M:%S Uhr')
          currentActivityEntry['time'] = formatTimedelta(end - start)
        currentActivity['entries'].append(currentActivityEntry)
    else:
      currentActivity['status'] = 'none'

    data = {
      'active_page': 'dashboard',
      'uid': user.getData('uid'),
      'username': user.getData('username'),
      'first_name': user.getData('first_name'),
      'last_name': user.getData('last_name'),
      'role': user.getData('role'),
      'img': user.getData('img'),
      'current_activity': currentActivity,
      'placeholder_module': {
        'name': modules[0]['modules'][0]['submodules'][0]['name'],
        'index': modules[0]['modules'][0]['submodules'][0]['index']
      },
      'modules': modules,
      'last_reports': lastReports,
      'total_time': reviewData['totalTime'],
      'total_sessions': reviewData['totalSessions'],
      'review_data': reviewData['reviewDataJSON'],
      'requests': User.getFormattedRequests(),
      'requested_role': user.getData('requested_role')
    }

    if 'notification' in request.session:
      data['notification'] = request.session['notification']
      del request.session['notification']

    return render(request, 'dvmplanner/dashboard.html', data)
  
  else:
    return redirect(home)

def reports(request):
  if 'uid' in request.session:
    user = User.getUserByKey('uid', request.session['uid'])

    reports = []
    for report in user.getData('reports'):
      reports.append(report.getFormattedData())
    current_module = '[Alle]'
    current_semester = '[Alle]'

    data = {
      'active_page': 'reports',
      'uid': user.getData('uid'),
      'username': user.getData('username'),
      'first_name': user.getData('first_name'),
      'last_name': user.getData('last_name'),
      'role': user.getData('role'),
      'img': user.getData('img'),
      'current_module': current_module,
      'current_semester': current_semester,
      'modules': Submodule.getAllFormattedModules(),
      'reports': reports
    }

    if 'notification' in request.session:
      data['notification'] = request.session['notification']
      del request.session['notification']

    return render(request, 'dvmplanner/reports.html', data)
  
  else:
    return redirect(home)

def review(request):
  if 'uid' in request.session:
    user = User.getUserByKey('uid', request.session['uid'])

    reviewData = user.getFormattedReview()
    current_module = '[Alle]'
    current_semester = '[Alle]'

    data = {
      'active_page': 'review',
      'uid': user.getData('uid'),
      'username': user.getData('username'),
      'first_name': user.getData('first_name'),
      'last_name': user.getData('last_name'),
      'role': user.getData('role'),
      'img': user.getData('img'),
      'current_module': current_module,
      'current_semester': current_semester,
      'modules': Submodule.getAllFormattedModules(),
      'total_time': reviewData['totalTime'],
      'total_sessions': reviewData['totalSessions'],
      'reviews': reviewData['reviewData'],
      'review_data': reviewData['reviewDataJSON']
    }

    if 'notification' in request.session:
      data['notification'] = request.session['notification']
      del request.session['notification']

    return render(request, 'dvmplanner/review.html', data)
  
  else:
    return redirect(home)

def admin(request):
  if 'uid' in request.session:
    user = User.getUserByKey('uid', request.session['uid'])
    if user.getData('role') == 'admin':

      current_requests_filter_role = '[Alle]'
      current_users_filter_role = '[Alle]'
      current_users_filter_status = '[Alle]'

      users = []
      for userEntry in User.getUsers():
        users.append({
          'day': userEntry.getData('creation_date').strftime('%d.%m.%Y'),
          'time': userEntry.getData('creation_date').strftime('%H.%M:%S Uhr'),
          'first_name': userEntry.getData('first_name'),
          'last_name': userEntry.getData('last_name'),
          'username': userEntry.getData('username'),
          'role': userEntry.getData('role'),
          'status': userEntry.getData('status'),
          'id': userEntry.getData('uid')
        })

      data = {
        'active_page': 'admin',
        'uid': user.getData('uid'),
        'username': user.getData('username'),
        'first_name': user.getData('first_name'),
        'last_name': user.getData('last_name'),
        'role': user.getData('role'),
        'img': user.getData('img'),
        'current_requests_filter_role': current_requests_filter_role,
        'requests': User.getFormattedRequests(),
        'current_users_filter_role': current_users_filter_role,
        'current_users_filter_status': current_users_filter_status,
        'users': users,
        'modules': Submodule.getAllFormattedModules()
      }

      if 'notification' in request.session:
        data['notification'] = request.session['notification']
        del request.session['notification']

      return render(request, 'dvmplanner/admin.html', data)
      
    else:
      request.session['notification'] = f'Du hast keine Berechtigungen für das Admin Dashboard.'
      return redirect(dashboard)
    
  else:
    return redirect(home)

def profile(request):
  if 'uid' in request.session:
    user = User.getUserByKey('uid', request.session['uid'])
    data = {
      'active_page': 'profile',
      'uid': user.getData('uid'),
      'username': user.getData('username'),
      'first_name': user.getData('first_name'),
      'last_name': user.getData('last_name'),
      'role': user.getData('role'),
      'img': user.getData('img'),
      'email': user.getData('email'),
      'creation_date': user.getData('creation_date').strftime('%d.%m.%Y, %H.%M:%S Uhr'),
      'requested_role': user.getData('requested_role')
    }

    if 'notification' in request.session:
      data['notification'] = request.session['notification']
      del request.session['notification']

    return render(request, 'dvmplanner/profile.html', data)
  
  else:
    return redirect(home)

def addreport(request):
  if 'uid' in request.session:
    user = User.getUserByKey('uid', request.session['uid'])

    modules = Submodule.getAllFormattedModules()

    data = {
      'active_page': 'addreport',
      'uid': user.getData('uid'),
      'username': user.getData('username'),
      'first_name': user.getData('first_name'),
      'last_name': user.getData('last_name'),
      'role': user.getData('role'),
      'img': user.getData('img'),
      'placeholder_module': {
        'name': modules[0]['modules'][0]['submodules'][0]['name'],
        'index': modules[0]['modules'][0]['submodules'][0]['index']
      },
      'modules': modules
    }

    if 'notification' in request.session:
      data['notification'] = request.session['notification']
      del request.session['notification']

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
        data = { 'notification': 'Falsches Passwort!' }
        return render(request, 'dvmplanner/login.html', data)
      
    else:
      data = { 'notification': 'Falscher Benutzername oder E-Mail!' }
      return render(request, 'dvmplanner/login.html', data)
    
  else:
    data = {}
    if 'notification' in request.session:
      data['notification'] = request.session['notification']
      del request.session['notification']

    return render(request, 'dvmplanner/login.html', data)

def signup(request):
  if request.POST.get('context', '') == 'signup':
    username = request.POST.get('username', '')
    firstName = request.POST.get('first_name', '')
    lastName = request.POST.get('last_name', '')
    email = request.POST.get('email', '')
    pwd = request.POST.get('pwd', '')
    pwdRepeat = request.POST.get('pwd_repeat', '')

    if User.getUserByKey('email', email):
      data = { 'notification': 'Die E-Mail ist bereits vergeben!' }
      return render(request, 'dvmplanner/signup.html', data)
    
    elif User.getUserByKey('username', username):
      data = { 'notification': 'Der Benutzername ist bereits vergeben!' }
      return render(request, 'dvmplanner/signup.html', data)
    
    elif pwd != pwdRepeat:
      data = { 'notification': 'Die Passwörter stimmen nicht überein!' }
      return render(request, 'dvmplanner/signup.html', data)
    
    else:
      user = User.createUser(username, firstName, lastName, email, pwd)
      request.session['uid'] = user.getData('uid')
      request.session['notification'] = f'Der Benutzer { username } wurde erfolgreich angelegt.'
      return redirect(dashboard)
    
  else:
    data = {}
    if 'notification' in request.session:
      data['notification'] = request.session['notification']
      del request.session['notification']

    return render(request, 'dvmplanner/signup.html', data)