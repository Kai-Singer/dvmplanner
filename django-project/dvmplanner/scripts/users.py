from dvmplanner.scripts.main import BASE_DIR
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
      userobj = User(user['uid'], user['username'], user['first_name'], user['last_name'], user['email'], user['pwd'], creation_date, user['img'], user['role'], user['requested_role'], user['status'], user['current_activity'])
      reports = Report.getUserReports(userobj)
      userobj.updateReports(reports)
      users.append(userobj)
      file.close()
    return users

  @staticmethod
  def getUserByLogin(login: str):
    result = None
    for user in User.getUsers():
      if user.getUsername() == login or user.getEmail() == login:
        result = user
    return result
  
  @staticmethod
  def getUserByUsername(username: str):
    result = None
    for user in User.getUsers():
      if user.getUsername() == username:
        result = user
    return result
  
  @staticmethod
  def getUserByEmail(email: str):
    result = None
    for user in User.getUsers():
      if user.getEmail() == email:
        result = user
    return result
  
  @staticmethod
  def createUser(username: str, first_name: str, last_name: str, email: str, pwd: str):
    uid = 0
    for user in User.getUsers():
      userUid = user.getUid()
      userUid = int(userUid[1:])
      if userUid > uid:
        uid = userUid
    uid = f'u{str(uid + 1).zfill(4)}'
    creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    createdUser = User(uid, username, first_name, last_name, email, pwd, creation_date, False, 'normal', '', 'active', { 'status': 'none' })
    createdUser.updateJSON()
    return createdUser

  def __init__(self, uid: str, username: str, first_name: str, last_name: str, email: str, pwd: str, creation_date: datetime, img: bool, role: str, requested_role: str, status: str, current_activity: dict, reports: list['Report'] = []):
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
    self.__status = status
    self.__current_activity = current_activity
    self.__reports = reports

  def getUid(self):
    return self.__uid
  
  def getUsername(self):
    return self.__username
  
  def getEmail(self):
    return self.__email
  
  def updateReports(self, reports: list['Report']):
    self.__reports = reports

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
      'creation_date': self.__creation_date,
      'img': self.__img,
      'role': self.__role,
      'requested_role': self.__requested_role,
      'status': self.__status,
      'current_activity': self.__current_activity
    }
    userspath = BASE_DIR + '/data/users/'
    file = open(os.path.join(userspath, f'{self.__uid}.json'), 'w', encoding = 'utf-8')
    file.write(json.dumps(data, indent = 2))
    file.close()
  
class Report:
  @staticmethod
  def getUserReports(user: User):
    reports = []
    uid = user.getUid()
    path = f'{BASE_DIR}/data/reports/{uid}.csv'
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