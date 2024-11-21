import os, json

class User:
  def __init__(self, username, first_name, last_name, email, pwd, status, blocked):
    self.__username = username
    self.__first_name = first_name
    self.__last_name = last_name
    self.__email = email
    self.__pwd = pwd
    self.__status = status
    self.__blocked = blocked

  def getUsername(self):
    return self.__username
  
def getUsers():
  users = []
  userspath = 'dvmplanner/data/users'
    
  for filename in os.listdir(userspath):
    path = os.path.join(userspath, filename)
    file = open(path, 'r', encoding = 'utf-8')
    user = json.loads(file.read())
    userobj = User(user['username'], user['first_name'], user['last_name'], user['email'], user['pwd'], user['status'], user['blocked'])
    users.append(userobj)
    file.close()
  
  return users