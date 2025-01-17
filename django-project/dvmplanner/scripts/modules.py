from dvmplanner.scripts.main import BASE_DIR
from lxml import etree
from io import StringIO

class Submodule:
  @staticmethod
  def getAllFormattedModules():
    allModules = []
    moduleGroups = ModuleGroup.getModuleGroups()
    for moduleGroup in moduleGroups:
      modules = []
      for module in moduleGroup.getData('modules'):
        submodules = []
        for submodule in module.getData('submodules'):
          submodules.append({
            'index': submodule.getCompleteIndex(),
            'name': submodule.getData('name'),
            'semester': submodule.getData('semester')
          })
        modules.append({
          'index': module.getCompleteIndex(),
          'name': module.getData('name'),
          'submodules': submodules
        })
      allModules.append({
        'index': moduleGroup.getIndex(),
        'name': moduleGroup.getData('name'),
        'modules': modules
      })
    return allModules

  @staticmethod
  def getSubmodules(module: 'Module'):
    moduleIndex = module.getIndex()
    moduleGroupIndex = module.getModuleGroupIndex()
    submodules = []
    path = BASE_DIR + '/data/modules.xml'
    file = open(path, 'r', encoding = 'utf-8')
    xml = etree.parse(StringIO(file.read()))
    file.close()
    xpath = xml.xpath(f'/Modules/ModuleGroup[@index = "{ moduleGroupIndex }"]/Module[@index = "{ moduleIndex }"]/Submodule')
    for submodule in xpath:
      submoduleobj = Submodule(submodule.attrib['index'], submodule.attrib['name'], submodule.attrib['semester'], module)
      submodules.append(submoduleobj)
    return submodules
  
  @staticmethod
  def getByIndex(index: str):
    indexSplit = index.split('.')
    result = None
    for moduleGroup in ModuleGroup.getModuleGroups():
      if moduleGroup.getIndex() == indexSplit[0]:
        for module in Module.getModules(moduleGroup):
          if module.getIndex() == indexSplit[1]:
            for submodule in Submodule.getSubmodules(module):
              if submodule.getIndex() == indexSplit[2]:
                result = submodule
    return result
    
  def __init__(self, index: int, name: str, semester: int, module: 'Module'):
    self.__index = index
    self.__name = name
    self.__semester = semester
    self.__module = module

  def getIndex(self):
    return self.__index
  
  def getCompleteIndex(self):
    return f'{ self.__module.getModuleGroupIndex() }.{ self.__module.getIndex() }.{ self.__index }'  
  
  def getData(self, keyName: str):
    data = {
      'index': self.__index,
      'name': self.__name,
      'semester': self.__semester,
      'module': self.__module
    }
    return data[keyName]

class Module:
  @staticmethod
  def getModules(moduleGroup: 'ModuleGroup'):
    moduleGroupIndex = moduleGroup.getIndex()
    modules = []
    path = BASE_DIR + '/data/modules.xml'
    file = open(path, 'r', encoding = 'utf-8')
    xml = etree.parse(StringIO(file.read()))
    file.close()
    xpath = xml.xpath(f'/Modules/ModuleGroup[@index = "{ moduleGroupIndex }"]/Module')
    for module in xpath:
      moduleobj = Module(module.attrib['index'], module.attrib['name'], moduleGroup)
      modules.append(moduleobj)
    return modules
    
  def __init__(self, index: int, name: str, moduleGroup: 'ModuleGroup'):
    self.__index = index
    self.__name = name
    self.__module_group = moduleGroup
    self.__submodules = Submodule.getSubmodules(self)

  def getIndex(self):
    return self.__index
  
  def getModuleGroupIndex(self):
    return self.__module_group.getIndex()
  
  def getCompleteIndex(self):
    return f'{ self.__module_group.getIndex() }.{ self.__index }'  
  
  def getData(self, keyName: str):
    data = {
      'index': self.__index,
      'name': self.__name,
      'module_group': self.__module_group,
      'submodules': self.__submodules
    }
    return data[keyName]

class ModuleGroup:
  @staticmethod
  def getModuleGroups():
    moduleGroups = []
    path = BASE_DIR + '/data/modules.xml'
    file = open(path, 'r', encoding = 'utf-8')
    xml = etree.parse(StringIO(file.read()))
    file.close()
    xpath = xml.xpath('/Modules/ModuleGroup')
    for moduleGroup in xpath:
      modulegroupobj = ModuleGroup(moduleGroup.attrib['index'], moduleGroup.attrib['name'])
      moduleGroups.append(modulegroupobj)
    return moduleGroups
    
  def __init__(self, index: int, name: str):
    self.__index = index
    self.__name = name
    self.__modules = Module.getModules(self)

  def getIndex(self):
    return self.__index
  
  def getData(self, keyName: str):
    data = {
      'index': self.__index,
      'name': self.__name,
      'modules': self.__modules
    }
    return data[keyName]