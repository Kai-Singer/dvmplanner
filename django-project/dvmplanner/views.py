from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from dvmplanner.scripts.users import User, Report
from dvmplanner.scripts.modules import Submodule, Module, ModuleGroup
from dvmplanner.scripts.main import BASE_DIR, formatTimedelta
from datetime import datetime
from lxml import etree
from io import StringIO
import os, json, csv, shutil

def home(request):
  if 'uid' in request.session:
    user = User.getUserByKey('uid', request.session['uid'])
    if user.getData('status') != 'blocked' and user.getData('status') != 'deleted':
      return redirect(dashboard)
    else:
      request.session.flush()
    
  data = {}
  if 'notification' in request.session:
    data['notification'] = request.session['notification']
    del request.session['notification']

  return render(request, 'dvmplanner/home.html', data)

def dashboard(request):
  if 'uid' in request.session:
    user = User.getUserByKey('uid', request.session['uid'])
    context = request.POST.get('context', '')

    if user.getData('status') == 'blocked':
      request.session.flush()
      request.session['notification'] = {
        'msg': 'Dein Profil ist gesperrt!',
        'success': False
      }
      return redirect(home)
    
    if user.getData('status') == 'deleted':
      request.session.flush()
      request.session['notification'] = {
        'msg': 'Das Profil wurde gelöscht!',
        'success': False
      }
      return redirect(home)

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

    if user.getData('status') == 'blocked':
      request.session.flush()
      request.session['notification'] = {
        'msg': 'Dein Profil ist gesperrt!',
        'success': False
      }
      return redirect(home)
    
    if user.getData('status') == 'deleted':
      request.session.flush()
      request.session['notification'] = {
        'msg': 'Das Profil wurde gelöscht!',
        'success': False
      }
      return redirect(home)

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
      uploadedFile = request.FILES['file']
      fileExt = os.path.splitext(uploadedFile.name)[1].lower()[1:]
      transferPath = f'{ BASE_DIR }/data/transfer/{ user.getData('uid') }'
      if not os.path.exists(transferPath):
        os.mkdir(transferPath)
      fs = FileSystemStorage(transferPath)
      filePath = os.path.join(transferPath, f'reportUpload.{fileExt}')
      if os.path.isfile(filePath):
        os.remove(filePath)
      fs.save(f'reportUpload.{fileExt}', uploadedFile)
      reports = []
      file = open(filePath, 'r', encoding = 'utf-8')
      try:
        if fileExt == 'xml':
          xml = etree.parse(StringIO(file.read()))
          xpath = xml.xpath(f'/reports/report')
          for report in xpath:
            start = datetime.strptime(report.attrib['start'], '%Y-%m-%d %H:%M:%S')
            end = datetime.strptime(report.attrib['end'], '%Y-%m-%d %H:%M:%S')
            if start > end:
              raise Exception('Die Startzeit muss vor der Endzeit sein!')
            if not (report.attrib['id'].startswith('r') and report.attrib['id'][1:].isdigit() and len(report.attrib['id']) == 5):
              raise Exception('Die Report ID ist nicht konform!')
            submodule = Submodule.getByIndex(report.attrib['submodule'])
            reportobj = Report(user, report.attrib['id'], start, end, submodule, report.attrib['notes'])
            reports.append(reportobj)
        elif fileExt == 'json':
          jsonReports = json.loads(file.read())['reports']
          for report in jsonReports:
            start = datetime.strptime(report['start'], '%Y-%m-%d %H:%M:%S')
            end = datetime.strptime(report['end'], '%Y-%m-%d %H:%M:%S')
            if start > end:
              raise Exception('Die Startzeit muss vor der Endzeit sein!')
            if not (report['id'].startswith('r') and report['id'][1:].isdigit() and len(report['id']) == 5):
              raise Exception('Die Report ID ist nicht konform!')
            submodule = Submodule.getByIndex(report['submodule'])
            reportobj = Report(user, report['id'], start, end, submodule, report['notes'])
            reports.append(reportobj)
        elif fileExt == 'csv':
          reader = csv.DictReader(file, delimiter = ';')
          for report in reader:
            start = datetime.strptime(report['start'], '%Y-%m-%d %H:%M:%S')
            end = datetime.strptime(report['end'], '%Y-%m-%d %H:%M:%S')
            if start > end:
              raise Exception('Die Startzeit muss vor der Endzeit sein!')
            if not (report['id'].startswith('r') and report['id'][1:].isdigit() and len(report['id']) == 5):
              raise Exception('Die Report ID ist nicht konform!')
            submodule = Submodule.getByIndex(report['submodule'])
            reportobj = Report(user, report['id'], start, end, submodule, report['notes'])
            reports.append(reportobj)
        user.updateReports(reports)
        user.updateReportCSV()
      except:
        request.session['notification'] = {
          'msg': 'Ein Problem mit der Formatierung oder den Zeiten besteht. Die Daten konnten nicht hochgeladen werden!',
          'success': False
        }
      file.close()
      os.remove(filePath)
      os.rmdir(transferPath)

    elif context == 'download_reports':
      filetype = request.POST.get('type', '')
      reports = user.getData('reports')
      userUid = user.getData('uid')

      if filetype == 'xml':
        root = etree.Element('reports')
        for report in reports:
          reportModule = report.getData('submodule')
          reportModuleIndex = '0.0.0'
          if reportModule is not None:
            reportModuleIndex = reportModule.getCompleteIndex()
          reportElement = etree.Element('report', id = report.getData('rid'), start = report.getData('start').strftime('%Y-%m-%d %H:%M:%S'), end = report.getData('end').strftime('%Y-%m-%d %H:%M:%S'), submodule = reportModuleIndex, notes = report.getData('notes'))
          root.append(reportElement)
        xmlData = etree.tostring(root, pretty_print = True, encoding = 'utf-8').decode()
        response = HttpResponse(xmlData, content_type='application/xml')
        response['Content-Disposition'] = f'attachment; filename="{ userUid }_reports.xml"'
        return response
      
      elif filetype == 'json':
        jsonData = {
          'reports': []
        }
        for report in reports:
          reportModule = report.getData('submodule')
          reportModuleIndex = '0.0.0'
          if reportModule is not None:
            reportModuleIndex = reportModule.getCompleteIndex()
          jsonData['reports'].append({
            'id': report.getData('rid'),
            'start': report.getData('start').strftime('%Y-%m-%d %H:%M:%S'),
            'end': report.getData('end').strftime('%Y-%m-%d %H:%M:%S'),
            'submodule': reportModuleIndex,
            'notes': report.getData('notes')
          })
        response = HttpResponse(json.dumps(jsonData, indent = 2), content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="{ userUid }_reports.json"'
        return response
      
      elif filetype == 'csv':
        csvData = StringIO()
        fieldnames = [ 'id', 'start', 'end', 'submodule', 'notes' ]
        writer = csv.DictWriter(csvData, fieldnames = fieldnames, delimiter = ';')
        writer.writeheader()
        for report in reports:
          reportModule = report.getData('submodule')
          reportModuleIndex = '0.0.0'
          if reportModule is not None:
            reportModuleIndex = reportModule.getCompleteIndex()
          writer.writerow({
            'id': report.getData('rid'),
            'start': report.getData('start').strftime('%Y-%m-%d %H:%M:%S'),
            'end': report.getData('end').strftime('%Y-%m-%d %H:%M:%S'),
            'submodule': reportModuleIndex,
            'notes': report.getData('notes'),
          })
        response = HttpResponse(csvData.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{ userUid }_reports.csv"'
        csvData.close()
        return response

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

    if user.getData('status') == 'blocked':
      request.session.flush()
      request.session['notification'] = {
        'msg': 'Dein Profil ist gesperrt!',
        'success': False
      }
      return redirect(home)
    
    if user.getData('status') == 'deleted':
      request.session.flush()
      request.session['notification'] = {
        'msg': 'Das Profil wurde gelöscht!',
        'success': False
      }
      return redirect(home)

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
    
    elif context == 'review_dropdown_select_module':
      index = request.POST.get('index', '')
      request.session['review_dropdown_select_module'] = index

    elif context == 'review_dropdown_select_semester':
      semester = request.POST.get('semester', '')
      request.session['review_dropdown_select_semester'] = semester

    selectedReports = user.getData('reports')
    current_module = '[Alle]'
    if 'review_dropdown_select_module' in request.session:
      requestModule = request.session['review_dropdown_select_module']
      if requestModule != 'all':
        if requestModule.count('.') == 0:
          module = ModuleGroup.getByIndex(requestModule)
          selectedReports = Report.getReportsByModuleGroup(module, selectedReports)
        else:
          module = Module.getByIndex(requestModule)
          selectedReports = Report.getReportsByModule(module, selectedReports)
        current_module = f'{ module.getCompleteIndex() } { module.getData('name') }'
    
    current_semester = '[Alle]'
    if 'review_dropdown_select_semester' in request.session:
      requestSemester = request.session['review_dropdown_select_semester']
      if requestSemester != 'all':
        selectedReports = Report.getReportsBySemester(requestSemester, selectedReports)
        current_semester = f'{requestSemester}. Semester'

    reviewData = user.getFormattedReview(selectedReports)

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

    if context == 'print_review':
      return render(request, 'dvmplanner/print_review.html', data)
  
    else:
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

    if user.getData('status') == 'blocked':
      request.session.flush()
      request.session['notification'] = {
        'msg': 'Dein Profil ist gesperrt!',
        'success': False
      }
      return redirect(home)
    
    if user.getData('status') == 'deleted':
      request.session.flush()
      request.session['notification'] = {
        'msg': 'Das Profil wurde gelöscht!',
        'success': False
      }
      return redirect(home)

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
      
      elif context == 'request_action':
        action = request.POST.get('action', '')
        userId = request.POST.get('id', '')
        requestUser = User.getUserByKey('uid', userId)

        if action == 'accept':
          requestUser.changeData('role', requestUser.getData('requested_role'))
          requestUser.changeData('requested_role', '')
          request.session['notification'] = {
            'msg': 'Die Anfrage wurde erfolgreich akzeptiert.',
            'success': True
          }

        elif action == 'decline':
          requestUser.changeData('requested_role', '')
          request.session['notification'] = {
            'msg': 'Die Anfrage wurde erfolgreich abgelehnt.',
            'success': True
          }

      elif context == 'change_role':
        role = request.POST.get('role', '')
        userId = request.POST.get('id', '')
        requestUser = User.getUserByKey('uid', userId)
        requestUser.changeData('requested_role', '')
        requestUser.changeData('role', role)
        if userId == user.getData('uid') and role != 'admin':
          request.session['notification'] = {
            'msg': 'Du hast keine Berechtigungen mehr für das Admin Dashboard.',
            'success': False
          }
          return redirect(dashboard)
        else:
          request.session['notification'] = {
            'msg': 'Die Rolle wurde erfolgreich geändert.',
            'success': True
          }

      elif context == 'block_user':
        action = request.POST.get('action', '')
        userId = request.POST.get('id', '')
        requestUser = User.getUserByKey('uid', userId)

        if action == 'block':
          requestUser.changeData('status', 'blocked')
          request.session['notification'] = {
            'msg': 'Der Benutzer wurde erfolgreich gesperrt.',
            'success': True
          }

        elif action == 'unblock':
          requestUser.changeData('status', 'active')
          request.session['notification'] = {
            'msg': 'Der Benutzer wurde erfolgreich entsperrt.',
            'success': True
          }

      elif context == 'edit_module':
        index = request.POST.get('index', '')
        semester = request.POST.get('semester', '')
        name = request.POST.get('name', '')
        if index.count('.') == 0:
          moduleGroup = ModuleGroup.getByIndex(index)
          moduleGroup.edit(name)
        elif index.count('.') == 1:
          module = Module.getByIndex(index)
          module.edit(name)
        else:
          submodule = Submodule.getByIndex(index)
          submodule.edit(name, semester)
        request.session['notification'] = {
          'msg': 'Das Modul wurde erfolgreich bearbeitet.',
          'success': True
        }

      elif context == 'delete_module':
        index = request.POST.get('index', '')
        if index.count('.') == 0:
          moduleGroup = ModuleGroup.getByIndex(index)
          moduleGroup.remove()
        elif index.count('.') == 1:
          module = Module.getByIndex(index)
          module.remove()
        else:
          submodule = Submodule.getByIndex(index)
          submodule.remove()
        request.session['notification'] = {
          'msg': 'Das Modul wurde erfolgreich gelöscht.',
          'success': True
        }

      elif context == 'add_module':
        index = request.POST.get('index', '')
        splittedIndex = index.split('.')
        semester = request.POST.get('semester', '')
        name = request.POST.get('name', '')
        error = ''
        if len(splittedIndex) < 1 or len(splittedIndex) > 3:
          error = 'format'
        for i in splittedIndex:
          if len(i) != 1:
            error = 'format'
          elif not i.isdigit():
            error = 'format'
        if len(splittedIndex) == 3:
          if Submodule.getByIndex(index) != None:
            error = 'used'
        elif len(splittedIndex) == 2:
          if Module.getByIndex(index) != None:
            error = 'used'
        elif len(splittedIndex) == 1:
          if ModuleGroup.getByIndex(index) != None:
            error = 'used'
        if error == 'format':
          request.session['notification'] = {
            'msg': 'Der Modulindex muss das Format "X.X.X" haben!',
            'success': False
          }
        elif error == 'used':
          request.session['notification'] = {
            'msg': 'Der Modulindex ist bereits vergeben!',
            'success': False
          }
        else:
          if len(splittedIndex) == 1:
            moduleGroup = ModuleGroup(splittedIndex[0], name)
            moduleGroup.addToXml()
          elif len(splittedIndex) == 2:
            moduleGroup = ModuleGroup.getByIndex(splittedIndex[0])
            module = Module(splittedIndex[1], name, moduleGroup)
            module.addToXml()
          else:
            module = Module.getByIndex(f'{ splittedIndex[0] }.{ splittedIndex[1] }')
            submodule = Submodule(splittedIndex[2], name, semester, module)
            submodule.addToXml()
          request.session['notification'] = {
            'msg': 'Das Modul wurde erfolgreich hinzugefügt.',
            'success': True
          }

      elif context == 'restore_default':
        path = f'{ BASE_DIR }/data/modules.xml'
        if os.path.exists(path):
          os.remove(path)
        shutil.copy(f'{ BASE_DIR }/data/z_modules_default.xml', path)
        request.session['notification'] = {
            'msg': 'Das Standard Modulhandbuch wurde erfolgreich geladen.',
            'success': True
          }    

      elif context == 'requests_dropdown_select_role':
        role = request.POST.get('role', '')
        request.session['requests_dropdown_select_role'] = role

      elif context == 'users_dropdown_select_role':
        role = request.POST.get('role', '')
        request.session['users_dropdown_select_role'] = role

      elif context == 'users_dropdown_select_status':
        status = request.POST.get('status', '')
        request.session['users_dropdown_select_status'] = status

      current_requests_filter_role = '[Alle]'
      if 'requests_dropdown_select_role' in request.session:
        requestRole = request.session['requests_dropdown_select_role']
        if requestRole == 'vip':
          requests = User.getFormattedRequests('vip')
          current_requests_filter_role = 'VIP'
        elif requestRole == 'admin':
          requests = User.getFormattedRequests('admin')
          current_requests_filter_role = 'Admin'
        else:
          requests = User.getFormattedRequests()
      else:
        requests = User.getFormattedRequests()

      current_users_filter_role = '[Alle]'
      if 'users_dropdown_select_role' in request.session:
        current_users_filter_role = {
          'all': '[Alle]',
          'normal': 'Normal',
          'vip': 'VIP',
          'admin': 'Admin'
        }[request.session['users_dropdown_select_role']]

      current_users_filter_status = '[Alle]'
      if 'users_dropdown_select_status' in request.session:
        current_users_filter_status = {
          'all': '[Alle]',
          'active': 'Aktiv',
          'blocked': 'Gesperrt',
          'deleted': 'Gelöscht'
        }[request.session['users_dropdown_select_status']]

      users = []
      for userEntry in User.getUsers():
        if 'users_dropdown_select_role' in request.session:
          requestRoleSelect = request.session['users_dropdown_select_role']
          if requestRoleSelect != 'all' and requestRoleSelect != userEntry.getData('role'):
            continue
        if 'users_dropdown_select_status' in request.session:
          requestStatusSelect = request.session['users_dropdown_select_status']
          if requestStatusSelect != 'all' and requestStatusSelect != userEntry.getData('status'):
            continue
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
        'requests': requests,
        'current_users_filter_role': current_users_filter_role,
        'current_users_filter_status': current_users_filter_status,
        'users': users,
        'modules': Submodule.getAllFormattedModules()
      }

      if 'notification' in request.session:
        data['notification'] = request.session['notification']
        del request.session['notification']

      if user.getData('role') == 'admin':
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

    if user.getData('status') == 'blocked':
      request.session.flush()
      request.session['notification'] = {
        'msg': 'Dein Profil ist gesperrt!',
        'success': False
      }
      return redirect(home)
    
    if user.getData('status') == 'deleted':
      request.session.flush()
      request.session['notification'] = {
        'msg': 'Das Profil wurde gelöscht!',
        'success': False
      }
      return redirect(home)

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
    
    elif context == 'edit_profile':
      username = request.POST.get('username', '')
      first_name = request.POST.get('first_name', '')
      last_name = request.POST.get('last_name', '')
      email = request.POST.get('email', '')

      if User.getUserByKey('email', email) and email != user.getData('email'):
        request.session['notification'] = {
          'msg': 'Die neue E-Mail ist bereits vergeben!',
          'success': False
        }
      elif User.getUserByKey('username', username) and username != user.getData('username'):
        request.session['notification'] = {
          'msg': 'Der neue Benutzername ist bereits vergeben!',
          'success': False
        }
      else:
        user.changeData('username', username)
        user.changeData('first_name', first_name)
        user.changeData('last_name', last_name)
        user.changeData('email', email)
        request.session['notification'] = {
          'msg': 'Die neuen Daten wurden erfolgreich bearbeitet.',
          'success': True
        }

    elif context == 'edit_password':
      old_pwd = request.POST.get('old_pwd', '')
      pwd = request.POST.get('pwd', '')
      pwd_repeat = request.POST.get('pwd_repeat', '')

      if user.checkPwd(old_pwd):
        if pwd == pwd_repeat:
          user.changeData('pwd', pwd)
          request.session['notification'] = {
            'msg': 'Das Passwort wurde erfolgreich geändert.',
            'success': True
          }
        else:
          request.session['notification'] = {
            'msg': 'Die neuen Passwörter stimmen nicht überein!',
            'success': False
          }
      else:
        request.session['notification'] = {
          'msg': 'Das eingegebene alte Passwort ist falsch!',
          'success': False
        }

    elif context == 'edit_picture':
      uploadedPicture = request.FILES['file']
      path = f'{ BASE_DIR }/static/profiles'
      fs = FileSystemStorage(path)
      filePath = os.path.join(path, f'{user.getData('uid')}.png')
      if os.path.isfile(filePath):
        os.remove(filePath)
      fs.save(f'{user.getData('uid')}.png', uploadedPicture)
      user.changeData('img', 'true')
      request.session['notification'] = {
        'msg': 'Das Profilbild wurde erfolgreich aktualisiert!',
        'success': True
      }

    elif context == 'remove_picture':
      filePath = f'{ BASE_DIR }/static/profiles/{user.getData('uid')}.png'
      if os.path.isfile(filePath):
        os.remove(filePath)
      user.changeData('img', 'false')
      request.session['notification'] = {
        'msg': 'Das Profilbild wurde erfolgreich entfernt!',
        'success': True
      }

    elif context == 'delete_profile':
      user.changeData('status', 'deleted')
      request.session.flush()
      request.session['notification'] = {
        'msg': 'Das Profil wurde erfolgreich gelöscht!',
        'success': True
      }
      return redirect(home)

    elif context == 'application':
      applicationType = request.POST.get('type', '')
      if applicationType != 'withdrawal':
        user.requestRole()
        request.session['notification'] = {
          'msg': 'Deine Bewerbung wurde erfolgreich abgeschickt!',
          'success': True
        }
      else:
        user.changeData('requested_role', '')
        request.session['notification'] = {
          'msg': 'Deine Bewerbung wurde erfolgreich zurückgezogen!',
          'success': True
        }
    
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

    if user.getData('status') == 'blocked':
      request.session.flush()
      request.session['notification'] = {
        'msg': 'Dein Profil ist gesperrt!',
        'success': False
      }
      return redirect(home)
    
    if user.getData('status') == 'deleted':
      request.session.flush()
      request.session['notification'] = {
        'msg': 'Das Profil wurde gelöscht!',
        'success': False
      }
      return redirect(home)

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
    
    elif context == 'add_report':
      time_beginn = request.POST.get('time_beginn', '')
      time_end = request.POST.get('time_end', '')
      module = request.POST.get('module', '')
      notes = request.POST.get('notes', '')
      time_beginn = datetime.strptime(time_beginn, '%Y-%m-%dT%H:%M')
      time_end = datetime.strptime(time_end, '%Y-%m-%dT%H:%M')
      if time_beginn > time_end:
        request.session['notification'] = {
          'msg': 'Die Startzeit muss vor der Endzeit sein!',
          'success': False
        }
      else:
        module = Submodule.getByIndex(module)
        user.addReport(time_beginn, time_end, module, notes)
        request.session['notification'] = {
          'msg': 'Der Arbeitsbericht wurde erfolgreich hinzugefügt.',
          'success': True
        }
    
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
      if user.getData('status') == 'active':
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
      
      elif user.getData('status') == 'blocked':
        data = {
          'notification': {
            'msg': 'Dein Profil ist gesperrt!',
            'success': False
          }
        }
        return render(request, 'dvmplanner/login.html', data)
      
      elif user.getData('status') == 'deleted':
        data = {
          'notification': {
            'msg': 'Das Profil wurde gelöscht!',
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