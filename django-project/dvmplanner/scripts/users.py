from dvmplanner.scripts.main import BASE_DIR, formatTimedelta
from dvmplanner.scripts.modules import Submodule
from datetime import datetime
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
      userobj = User(user['uid'], user['username'], user['first_name'], user['last_name'], user['email'], user['pwd'], creation_date, user['img'], user['role'], user['requested_role'], request_date, user['status'], user['current_activity'])
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
    creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    createdUser = User(uid, username, first_name, last_name, email, pwd, creation_date, False, 'normal', '', 'active', { 'status': 'none' })
    createdUser.updateJSON()
    return createdUser
  
  @staticmethod
  def getFormattedRequests():
    users = User.getUsers()
    requests = []
    for user in users:
      if user.getData('requested_role') != '':
        requests.append({
          'datetime': user.getData('request_date'),
          'day': user.getData('request_date').strftime('%d.%m.%Y'),
          'time': user.getData('request_date').strftime('%H.%M:%S Uhr'),
          'first_name': user.getData('first_name'),
          'last_name': user.getData('last_name'),
          'username': user.getData('username'),
          'role': user.getData('role'),
          'requested_role': user.getData('requested_role'),
          'id': user.getData('uid'),
        })
    requests = sorted(requests, key = lambda x: x['datetime'])
    for request in requests:
      del request['datetime']
    return requests

  def __init__(self, uid: str, username: str, first_name: str, last_name: str, email: str, pwd: str, creation_date: datetime, img: bool, role: str, requested_role: str, request_date: datetime, status: str, current_activity: dict, reports: list['Report'] = []):
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
    self.__current_activity = current_activity
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
      'current_activity': self.__current_activity,
      'reports': self.__reports
    }
    return data[keyName]
  
  def updateReports(self, reports: list['Report']):
    self.__reports = reports

  def checkPwd(self, pwd: str):
    return pwd == self.__pwd
  
  #! FÜR JSON FORMATIEREN!
  def updateJSON(self):
    data = {
      'uid': self.__uid,
      'username': self.__username,
      'first_name': self.__first_name,
      'last_name': self.__last_name,
      'email': self.__email,
      'pwd': self.__pwd,
      'creation_date': self.__creation_date,
      'img': self.__img,
      'role': self.__role,
      'requested_role': self.__requested_role,
      'request_date': self.__request_date,
      'status': self.__status,
      'current_activity': self.__current_activity
    }
    userspath = BASE_DIR + '/data/users/'
    file = open(os.path.join(userspath, f'{ self.__uid }.json'), 'w', encoding = 'utf-8')
    file.write(json.dumps(data, indent = 2))
    file.close()
  
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
    data = {
      'id': self.__rid,
      'day': startDay,
      'start': start,
      'end': end,
      'end_day': endDay,
      'time': formatTimedelta(self.__end - self.__start),
      'module_index': self.__submodule.getCompleteIndex(),
      'module_name': self.__submodule.getData('name'),
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