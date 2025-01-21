from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles import finders
from dvmplanner.scripts.users import User, Report
from dvmplanner.scripts.modules import Submodule, Module, ModuleGroup
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
    context = request.POST.get('context', '')

    if context == 'logout':
      request.session.flush()
      request.session['notification'] = {
        'msg': 'Du wurdest erfolgreich abgemeldet.',
        'success': True
      }
      return redirect(home)

    elif context == 'change_user':
      request.session.flush()
      request.session['notification'] = {
        'msg': 'Du wurdest erfolgreich abgemeldet.',
        'success': True
      }
      return redirect(login)

    elif context == 'start_report':
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

    elif context == 'pause_report':
      currentActivitySession = request.session['current_activity']
      currentActivitySession['status'] = 'paused'
      currentActivitySession['entries'][-1]['end'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      request.session['current_activity'] = currentActivitySession
      
    elif context == 'resume_report':
      currentActivitySession = request.session['current_activity']
      currentActivitySession['status'] = 'active'
      currentActivitySession['entries'].append({
        'start': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'end': ''
      })
      request.session['current_activity'] = currentActivitySession

    elif context == 'finish_report':
      currentActivitySession = request.session['current_activity']
      if currentActivitySession['status'] == 'active':
        currentActivitySession['entries'][-1]['end'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      currentActivitySession['status'] = 'finished'
      request.session['current_activity'] = currentActivitySession

    elif context == 'checkin_report':
      entries = request.session['current_activity']['entries']
      missingEnd = False
      for entry in entries:
        if entry['end'] == '':
          missingEnd = True
      if len(entries) <= 0:
        request.session['notification'] = {
          'msg': 'Du kannst einen Arbeitsbericht ohne aufgezeichnete Zeiten nicht abspeichern!',
          'success': False
        }
      elif missingEnd:
        request.session['notification'] = {
          'msg': 'Beende zuerst alle Zeiten bevor du den Arbeitsbericht abspeichern kannst!',
          'success': False
        }
      else:
        request.session['notification'] = {
          'msg': 'Der Arbeitsbericht wurde erfolgreich abgespeichert.',
          'success': True
        }
        moduleIndex = request.POST.get('module', '1.1.1')
        module = Submodule.getByIndex(moduleIndex)
        notes = request.POST.get('notes', '')
        for entry in entries:
          start = datetime.strptime(entry['start'], '%Y-%m-%d %H:%M:%S')
          end = datetime.strptime(entry['end'], '%Y-%m-%d %H:%M:%S')
          user.addReport(start, end, module, notes)
        del request.session['current_activity']

    elif context == 'delete_entries':
      del request.session['current_activity']

    elif context == 'delete_entry':
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
      currentActivityEntries = sorted(currentActivitySession['entries'], key = lambda x: x['start'], reverse = True)
      currentActivity['entries'] = []
      for entry in currentActivityEntries:
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
    request.session['notification'] = {
      'msg': 'Bitte melde dich zuerst an, bevor du auf diesen Bereich zugreifen kannst!',
      'success': False
    }
    return redirect(home)

def reports(request):
  if 'uid' in request.session:
    user = User.getUserByKey('uid', request.session['uid'])
    context = request.POST.get('context', '')

    if context == 'logout':
      request.session.flush()
      request.session['notification'] = {
        'msg': 'Du wurdest erfolgreich abgemeldet.',
        'success': True
      }
      return redirect(home)

    elif context == 'change_user':
      request.session.flush()
      request.session['notification'] = {
        'msg': 'Du wurdest erfolgreich abgemeldet.',
        'success': True
      }
      return redirect(login)
    
    elif context == 'edit_report':
      id = request.POST.get('id', '')
      time_beginn = request.POST.get('time_beginn', '')
      time_end = request.POST.get('time_end', '')
      module = request.POST.get('module', '')
      notes = request.POST.get('notes', '')
      report = user.getReportById(id)
      time_beginn = datetime.strptime(time_beginn, '%Y-%m-%dT%H:%M')
      time_end = datetime.strptime(time_end, '%Y-%m-%dT%H:%M')
      if time_beginn > time_end:
        request.session['notification'] = {
          'msg': 'Die Startzeit muss vor der Endzeit sein!',
          'success': False
        }
      else:
        module = Submodule.getByIndex(module)
        user.removeReport(report)
        user.addReport(time_beginn, time_end, module, notes)
        request.session['notification'] = {
          'msg': 'Der Arbeitsbericht wurde erfolgreich bearbeitet.',
          'success': True
        }

    elif context == 'delete_report':
      id = request.POST.get('id', '')
      report = user.getReportById(id)
      user.removeReport(report)
      request.session['notification'] = {
        'msg': 'Der Arbeitsbericht wurde erfolgreich gelöscht.',
        'success': True
      }

    elif context == 'upload_data':
      file = request.FILES['file']
      # fs = FileSystemStorage('rhabitApp/static/profiles')
      # if os.path.isfile(f'rhabitApp/static/profiles/{uid}.png'):
      #   os.remove(f'rhabitApp/static/profiles/{uid}.png')
      # fs.save(f'{uid}.png', file)
      pass

    elif context == 'download_reports':
      filetype = request.POST.get('type', '')
      pass

    elif context == 'reports_dropdown_select_module':
      index = request.POST.get('index', '')
      request.session['reports_dropdown_select_module'] = index

    elif context == 'reports_dropdown_select_semester':
      semester = request.POST.get('semester', '')
      request.session['reports_dropdown_select_semester'] = semester

    selectedReports = user.getData('reports')
    current_module = '[Alle]'
    if 'reports_dropdown_select_module' in request.session:
      requestModule = request.session['reports_dropdown_select_module']
      if requestModule != 'all':
        if requestModule.count('.') == 0:
          module = ModuleGroup.getByIndex(requestModule)
          selectedReports = Report.getReportsByModuleGroup(module, selectedReports)
        elif requestModule.count('.') == 1:
          module = Module.getByIndex(requestModule)
          selectedReports = Report.getReportsByModule(module, selectedReports)
        else:
          module = Submodule.getByIndex(requestModule)
          selectedReports = Report.getReportsBySubmodule(module, selectedReports)
        current_module = f'{ module.getCompleteIndex() } { module.getData('name') }'
    
    current_semester = '[Alle]'
    if 'reports_dropdown_select_semester' in request.session:
      requestSemester = request.session['reports_dropdown_select_semester']
      if requestSemester != 'all':
        selectedReports = Report.getReportsBySemester(requestSemester, selectedReports)
        current_semester = f'{requestSemester}. Semester'
    
    reports = []
    reportsRaw = sorted(selectedReports, key = lambda x: x.getData('start'), reverse = True)
    for report in reportsRaw:
      reports.append(report.getFormattedData())

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
    request.session['notification'] = {
      'msg': 'Bitte melde dich zuerst an, bevor du auf diesen Bereich zugreifen kannst!',
      'success': False
    }
    return redirect(home)

def review(request):
  if 'uid' in request.session:
    user = User.getUserByKey('uid', request.session['uid'])
    context = request.POST.get('context', '')

    if context == 'logout':
      request.session.flush()
      request.session['notification'] = {
        'msg': 'Du wurdest erfolgreich abgemeldet.',
        'success': True
      }
      return redirect(home)

    elif context == 'change_user':
      request.session.flush()
      request.session['notification'] = {
        'msg': 'Du wurdest erfolgreich abgemeldet.',
        'success': True
      }
      return redirect(login)

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
    request.session['notification'] = {
      'msg': 'Bitte melde dich zuerst an, bevor du auf diesen Bereich zugreifen kannst!',
      'success': False
    }
    return redirect(home)

def admin(request):
  if 'uid' in request.session:
    user = User.getUserByKey('uid', request.session['uid'])

    if user.getData('role') == 'admin':
      context = request.POST.get('context', '')

      if context == 'logout':
        request.session.flush()
        request.session['notification'] = {
          'msg': 'Du wurdest erfolgreich abgemeldet.',
          'success': True
        }
        return redirect(home)

      elif context == 'change_user':
        request.session.flush()
        request.session['notification'] = {
          'msg': 'Du wurdest erfolgreich abgemeldet.',
          'success': True
        }
        return redirect(login)

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
      request.session['notification'] = {
        'msg': 'Du hast keine Berechtigungen für das Admin Dashboard.',
        'success': False
      }
      return redirect(dashboard)
    
  else:
    request.session['notification'] = {
      'msg': 'Bitte melde dich zuerst an, bevor du auf diesen Bereich zugreifen kannst!',
      'success': False
    }
    return redirect(home)

def profile(request):
  if 'uid' in request.session:
    user = User.getUserByKey('uid', request.session['uid'])
    context = request.POST.get('context', '')

    if context == 'logout':
      request.session.flush()
      request.session['notification'] = {
        'msg': 'Du wurdest erfolgreich abgemeldet.',
        'success': True
      }
      return redirect(home)

    elif context == 'change_user':
      request.session.flush()
      request.session['notification'] = {
        'msg': 'Du wurdest erfolgreich abgemeldet.',
        'success': True
      }
      return redirect(login)
    
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
    request.session['notification'] = {
      'msg': 'Bitte melde dich zuerst an, bevor du auf diesen Bereich zugreifen kannst!',
      'success': False
    }
    return redirect(home)

def addreport(request):
  if 'uid' in request.session:
    user = User.getUserByKey('uid', request.session['uid'])
    context = request.POST.get('context', '')

    if context == 'logout':
      request.session.flush()
      request.session['notification'] = {
        'msg': 'Du wurdest erfolgreich abgemeldet.',
        'success': True
      }
      return redirect(home)

    elif context == 'change_user':
      request.session.flush()
      request.session['notification'] = {
        'msg': 'Du wurdest erfolgreich abgemeldet.',
        'success': True
      }
      return redirect(login)
    
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
    request.session['notification'] = {
      'msg': 'Bitte melde dich zuerst an, bevor du auf diesen Bereich zugreifen kannst!',
      'success': False
    }
    return redirect(home)

def login(request):
  context = request.POST.get('context', '')

  if context == 'login':
    username = request.POST.get('username', '')
    pwd = request.POST.get('pwd', '')

    user = User.getUserByKey('username', username)
    if user is None:
      user = User.getUserByKey('email', username)

    if user is not None:
      if user.checkPwd(pwd):
        request.session['uid'] = user.getData('uid')
        request.session['notification'] = {
          'msg': f'Erfolgreich als { user.getData('username') } angemeldet.',
          'success': True
        }
        return redirect(dashboard)
      
      else:
        data = {
          'notification': {
            'msg': 'Falsches Passwort!',
            'success': False
          }
        }
        return render(request, 'dvmplanner/login.html', data)
      
    else:
      data = {
        'notification': {
          'msg': 'Falscher Benutzername oder E-Mail!',
          'success': False
        }
      }
      return render(request, 'dvmplanner/login.html', data)
    
  else:
    data = {}
    if 'notification' in request.session:
      data['notification'] = request.session['notification']
      del request.session['notification']

    return render(request, 'dvmplanner/login.html', data)

def signup(request):
  context = request.POST.get('context', '')

  if context == 'signup':
    username = request.POST.get('username', '')
    firstName = request.POST.get('first_name', '')
    lastName = request.POST.get('last_name', '')
    email = request.POST.get('email', '')
    pwd = request.POST.get('pwd', '')
    pwdRepeat = request.POST.get('pwd_repeat', '')

    if User.getUserByKey('email', email):
      data = {
        'notification': {
          'msg': 'Die E-Mail ist bereits vergeben!',
          'success': False
        }
      }
      return render(request, 'dvmplanner/signup.html', data)
    
    elif User.getUserByKey('username', username):
      data = {
        'notification': {
          'msg': 'Der Benutzername ist bereits vergeben!',
          'success': False
        }
      }
      return render(request, 'dvmplanner/signup.html', data)
    
    elif pwd != pwdRepeat:
      data = {
        'notification': {
          'msg': 'Die Passwörter stimmen nicht überein!',
          'success': False
        }
      }
      return render(request, 'dvmplanner/signup.html', data)
    
    else:
      user = User.createUser(username, firstName, lastName, email, pwd)
      request.session['uid'] = user.getData('uid')
      request.session['notification'] = {
        'msg': f'Der Benutzer { username } wurde erfolgreich angelegt.',
        'success': True
      }
      return redirect(dashboard)
    
  else:
    data = {}
    if 'notification' in request.session:
      data['notification'] = request.session['notification']
      del request.session['notification']

    return render(request, 'dvmplanner/signup.html', data)