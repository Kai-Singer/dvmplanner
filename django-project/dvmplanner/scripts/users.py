from dvmplanner.scripts.main import BASE_DIR, formatTimedelta
from dvmplanner.scripts.modules import Submodule, Module, ModuleGroup
from datetime import datetime, timedelta
import os, json, csv

class User:
  @staticmethod
  def getUsers():
    users = []
    userspath = BASE_DIR + '/data/users'
    for filename in os.listdir(userspath):
      path = os.path.join(userspath, filename)
      file = open(path, 'r', encoding = 'utf-8')
      user = json.loads(file.read())
      creation_date = datetime.strptime(user['creation_date'], '%Y-%m-%d %H:%M:%S')
      request_date = datetime.strptime(user['request_date'], '%Y-%m-%d %H:%M:%S')
      userobj = User(user['uid'], user['username'], user['first_name'], user['last_name'], user['email'], user['pwd'], creation_date, user['img'], user['role'], user['requested_role'], request_date, user['status'])
      reports = Report.getUserReports(userobj)
      userobj.updateReports(reports)
      users.append(userobj)
      file.close()
    return users

  @staticmethod
  def getUserByKey(keyName: str, content: str):
    result = None
    for user in User.getUsers():
      if user.getData(keyName) == content:
        result = user
    return result
  
  @staticmethod
  def createUser(username: str, first_name: str, last_name: str, email: str, pwd: str):
    uid = 0
    for user in User.getUsers():
      userUid = user.getData('uid')
      userUid = int(userUid[1:])
      if userUid > uid:
        uid = userUid
    uid = f'u{ str(uid + 1).zfill(4) }'
    createdUser = User(uid, username, first_name, last_name, email, pwd, datetime.now(), False, 'normal', '', datetime.now(), 'active')
    createdUser.updateJSON()
    createdUser.updateReportCSV()
    return createdUser
  
  @staticmethod
  def getFormattedRequests(filter: str = None):
    users = User.getUsers()
    requests = []
    for user in users:
      userRequestRole = user.getData('requested_role')
      if userRequestRole != '':
        if (filter != None and userRequestRole == filter) or filter == None:
          requests.append({
            'datetime': user.getData('request_date'),
            'day': user.getData('request_date').strftime('%d.%m.%Y'),
            'time': user.getData('request_date').strftime('%H.%M:%S Uhr'),
            'first_name': user.getData('first_name'),
            'last_name': user.getData('last_name'),
            'username': user.getData('username'),
            'role': user.getData('role'),
            'requested_role': userRequestRole,
            'id': user.getData('uid'),
          })
    requests = sorted(requests, key = lambda x: x['datetime'])
    for request in requests:
      del request['datetime']
    return requests

  def __init__(self, uid: str, username: str, first_name: str, last_name: str, email: str, pwd: str, creation_date: datetime, img: bool, role: str, requested_role: str, request_date: datetime, status: str,reports: list['Report'] = []):
    self.__uid = uid
    self.__username = username
    self.__first_name = first_name
    self.__last_name = last_name
    self.__email = email
    self.__pwd = pwd
    self.__creation_date = creation_date
    self.__img = img
    self.__role = role
    self.__requested_role = requested_role
    self.__request_date = request_date
    self.__status = status
    self.__reports = reports

  def getData(self, keyName: str):
    data = {
      'uid': self.__uid,
      'username': self.__username,
      'first_name': self.__first_name,
      'last_name': self.__last_name,
      'email': self.__email,
      'creation_date': self.__creation_date,
      'img': self.__img,
      'role': self.__role,
      'requested_role': self.__requested_role,
      'request_date': self.__request_date,
      'status': self.__status,
      'reports': self.__reports
    }
    return data[keyName]
  
  def changeData(self, keyName: str, newData: str):
    if keyName == 'username':
      self.__username = newData
    elif keyName == 'first_name':
      self.__first_name = newData
    elif keyName == 'last_name':
      self.__last_name = newData
    elif keyName == 'email':
      self.__email = newData
    elif keyName == 'pwd':
      self.__pwd = newData
    elif keyName == 'img':
      if newData == 'true':
        self.__img = True
      elif newData == 'false':
        self.__img = False
    elif keyName == 'role':
      self.__role = newData
    elif keyName == 'requested_role':
      self.__requested_role = newData
    elif keyName == 'status':
      self.__status = newData
    self.updateJSON()

  def requestRole(self):
    if self.__role == 'normal':
      self.__requested_role = 'vip'
    elif self.__role == 'vip':
      self.__requested_role = 'admin'
    self.__request_date = datetime.now()
    self.updateJSON()
  
  def updateReports(self, reports: list['Report']):
    self.__reports = reports

  def addReport(self, start: datetime, end: datetime, submodule: Submodule, notes: str):
    rid = 0
    for reportEntry in self.__reports:
      entryRid = int(reportEntry.getData('rid')[1:])
      if entryRid > rid:
        rid = entryRid
    rid = f'r{str(rid + 1).zfill(4)}'
    report = Report(self, rid, start, end, submodule, notes)
    self.__reports.append(report)
    self.updateReportCSV()

  def getReportById(self, id: str):
    report = None
    for reportEntry in self.getData('reports'):
      if reportEntry.getData('rid') == id:
        report = reportEntry
    return report
  
  def removeReport(self, report: 'Report'):
    newReportList = self.getData('reports')
    for reportIndex, reportEntry in enumerate(newReportList):
      if reportEntry.getData('rid') == report.getData('rid'):
        del newReportList[reportIndex]
    self.updateReports(newReportList)
    self.updateReportCSV()

  def checkPwd(self, pwd: str):
    return pwd == self.__pwd
  
  def updateJSON(self):
    data = {
      'uid': self.__uid,
      'username': self.__username,
      'first_name': self.__first_name,
      'last_name': self.__last_name,
      'email': self.__email,
      'pwd': self.__pwd,
      'creation_date': self.__creation_date.strftime('%Y-%m-%d %H:%M:%S'),
      'img': self.__img,
      'role': self.__role,
      'requested_role': self.__requested_role,
      'request_date': self.__request_date.strftime('%Y-%m-%d %H:%M:%S'),
      'status': self.__status
    }
    userspath = BASE_DIR + '/data/users/'
    file = open(os.path.join(userspath, f'{ self.__uid }.json'), 'w', encoding = 'utf-8')
    file.write(json.dumps(data, indent = 2))
    file.close()

  def updateReportCSV(self):
    fieldnames = [ 'id', 'start', 'end', 'submodule', 'notes' ]
    path = f'{ BASE_DIR }/data/reports/{ self.__uid }.csv'
    file = open(path, 'w', newline = '', encoding = 'utf-8')
    writer = csv.DictWriter(file, fieldnames = fieldnames, delimiter = ';')
    writer.writeheader()
    for report in self.__reports:
      if report.getData('submodule') == None:
        moduleIndex = '0.0.0'
      else:
        moduleIndex = report.getData('submodule').getCompleteIndex()
      writer.writerow({
        'id': report.getData('rid'),
        'start': report.getData('start').strftime('%Y-%m-%d %H:%M:%S'),
        'end': report.getData('end').strftime('%Y-%m-%d %H:%M:%S'),
        'submodule': moduleIndex,
        'notes': report.getData('notes'),
      })
    file.close()

  def getFormattedReview(self, reportsList: list['Report'] = None):
    if reportsList == None:
      reportsList = self.__reports
    totalTime = timedelta(0)
    totalSessions = 0
    reviewDataRaw = {}
    for report in reportsList:
      totalTime += report.getData('end') - report.getData('start')
      totalSessions += 1
      if report.getData('submodule') == None:
        moduleIndex = '0.0.0'
      else:
        moduleIndex = report.getData('submodule').getCompleteIndex()
      if moduleIndex not in reviewDataRaw:
        reviewDataRaw[moduleIndex] = {
          'time': timedelta(0),
          'sessions': 0
        }
      reviewDataRaw[moduleIndex]['time'] += report.getData('end') - report.getData('start')
      reviewDataRaw[moduleIndex]['sessions'] += 1
    formattedTotalTime = formatTimedelta(totalTime)
    reviewDataJSON = []
    reviewData = []
    sortedReviewDataRaw = {}
    for key in sorted(reviewDataRaw):
      sortedReviewDataRaw[key] = reviewDataRaw[key]
    for module in sortedReviewDataRaw:
      submodule = Submodule.getByIndex(module)
      time = sortedReviewDataRaw[module]['time']
      if submodule == None:
        moduleNameRaw = '[GELÖSCHTES MODUL]'
        moduleSemester = '?'
      else:
        moduleNameRaw = submodule.getData('name')
        moduleSemester = str(submodule.getData('semester'))
      moduleName = f'{ module } { moduleNameRaw }'
      sessions = sortedReviewDataRaw[module]['sessions']
      reviewDataJSON.append({
        'module': moduleName,
        'time': formatTimedelta(time),
        'sessions': sessions
      })
      percentage = (time.total_seconds() / totalTime.total_seconds()) * 100
      percentage = f'{percentage:.2f}'.replace('.', ',') + ' %'
      reviewData.append({
        'module': moduleName,
        'semester': moduleSemester,
        'time': formatTimedelta(time),
        'percentage': percentage,
        'sessions': sessions
      })
    return {
      'totalTime': formattedTotalTime,
      'totalSessions': totalSessions,
      'reviewData': reviewData,
      'reviewDataJSON': json.dumps(reviewDataJSON)
    }
  
class Report:
  @staticmethod
  def getUserReports(user: User):
    reports = []
    path = f'{ BASE_DIR }/data/reports/{ user.getData('uid') }.csv'
    file = open(path, 'r', encoding = 'utf-8')
    reader = csv.DictReader(file, delimiter = ';')
    for report in reader:
      start = datetime.strptime(report['start'], '%Y-%m-%d %H:%M:%S')
      end = datetime.strptime(report['end'], '%Y-%m-%d %H:%M:%S')
      submodule = Submodule.getByIndex(report['submodule'])
      reportobj = Report(user, report['id'], start, end, submodule, report['notes'])
      reports.append(reportobj)
    file.close()
    return reports
  
  @staticmethod
  def getReportsBySemester(semester: int, selectedReports: list['Report']):
    newSelectedReports = []
    for report in selectedReports:
      reportSubmodule = report.getData('submodule')
      if reportSubmodule != None:
        if semester == reportSubmodule.getData('semester'):
          newSelectedReports.append(report)
    return newSelectedReports

  @staticmethod
  def getReportsByModuleGroup(moduleGroup: ModuleGroup, selectedReports: list['Report']):
    newSelectedReports = []
    for report in selectedReports:
      reportSubmodule = report.getData('submodule')
      if reportSubmodule != None:
        if moduleGroup.getIndex() == reportSubmodule.getModuleGroup().getIndex():
          newSelectedReports.append(report)
    return newSelectedReports

  @staticmethod
  def getReportsByModule(module: Module, selectedReports: list['Report']):
    newSelectedReports = []
    for report in selectedReports:
      reportSubmodule = report.getData('submodule')
      if reportSubmodule != None:
        if module.getIndex() == reportSubmodule.getModule().getIndex() and module.getModuleGroup().getIndex() == reportSubmodule.getModuleGroup().getIndex():
          newSelectedReports.append(report)
    return newSelectedReports

  @staticmethod
  def getReportsBySubmodule(submodule: Submodule, selectedReports: list['Report']):
    newSelectedReports = []
    for report in selectedReports:
      reportSubmodule = report.getData('submodule')
      if reportSubmodule != None:
        if submodule.getIndex() == reportSubmodule.getIndex() and submodule.getModule().getIndex() == reportSubmodule.getModule().getIndex() and submodule.getModuleGroup().getIndex() == reportSubmodule.getModuleGroup().getIndex():
          newSelectedReports.append(report)
    return newSelectedReports
  
  def __init__(self, user: User, rid: str, start: datetime, end: datetime, submodule: 'Submodule', notes: str):
    self.__user = user
    self.__rid = rid
    self.__start = start
    self.__end = end
    self.__submodule = submodule
    self.__notes = notes

  def getFormattedData(self):
    startDay = self.__start.strftime('%d.%m.%Y')
    start = self.__start.strftime('%H.%M:%S Uhr')
    endDay = self.__end.strftime('%d.%m.%Y')
    end = self.__end.strftime('%H.%M:%S Uhr')
    if startDay == endDay:
      endDay = ''
    if len(self.__notes) > 25:
      notes = f'{ self.__notes[:22] }...'
      longNotes = self.__notes
    else:
      notes = self.__notes
      longNotes = ''
    if self.__submodule == None:
      moduleIndex = '0.0.0'
      moduleName = '[GELÖSCHTES MODUL]'
    else:
      moduleIndex = self.__submodule.getCompleteIndex()
      moduleName = self.__submodule.getData('name')
    data = {
      'id': self.__rid,
      'day': startDay,
      'start': start,
      'end': end,
      'end_day': endDay,
      'time': formatTimedelta(self.__end - self.__start),
      'module_index': moduleIndex,
      'module_name': moduleName,
      'notes': notes,
      'long_notes': longNotes
    }
    return data
  
  def getData(self, keyName: str):
    data = {
      'user': self.__user,
      'rid': self.__rid,
      'start': self.__start,
      'end': self.__end,
      'submodule': self.__submodule,
      'notes': self.__notes
    }
    return data[keyName]