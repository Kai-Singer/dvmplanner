from dvmplanner.scripts.main import BASE_DIR
from datetime import datetime
import os, json

class User:
  @staticmethod
  def getUsers():
    users = []
    userspath = BASE_DIR + '/data/users'
    for filename in os.listdir(userspath):
      path = os.path.join(userspath, filename)
      file = open(path, 'r', encoding = 'utf-8')
      user = json.loads(file.read())
      userobj = User(user['username'], user['first_name'], user['last_name'], user['email'], user['pwd'], user['status'], user['blocked'])
      users.append(userobj)
      file.close()
    return users

  def __init__(self, username: str, first_name: str, last_name: str, email: str, pwd: str, status: str, blocked: bool, reports: list['Report']):
    self.__username = username
    self.__first_name = first_name
    self.__last_name = last_name
    self.__email = email
    self.__pwd = pwd
    self.__status = status
    self.__blocked = blocked
    self.__reports = reports

  def getUsername(self):
    return self.__username
  
class Report:
  def __init__(self, user: User, start: datetime, end: datetime, submodule: 'Submodule', notes: str):
    self.__user = user
    self.__start = start
    self.__end = end
    self.__submodule = submodule
    self.__notes = notes