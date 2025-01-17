from dvmplanner.scripts.main import BASE_DIR
from lxml import etree
from io import StringIO

class Submodule:
  @staticmethod
  def getSubmodules(module: 'Module'):
    moduleIndex = module.getIndex()
    moduleGroupIndex = module.getModuleGroupIndex()
    submodules = []
    path = BASE_DIR + '/data/modules.xml'
    file = open(path, 'r', encoding = 'utf-8')
    xml = etree.parse(StringIO(file.read()))
    file.close()
    xpath = xml.xpath(f'/Modules/ModuleGroup[@index = "{moduleGroupIndex}"]/Module[@index = "{moduleIndex}"]/Submodule')
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

class Module:
  @staticmethod
  def getModules(moduleGroup: 'ModuleGroup'):
    moduleGroupIndex = moduleGroup.getIndex()
    modules = []
    path = BASE_DIR + '/data/modules.xml'
    file = open(path, 'r', encoding = 'utf-8')
    xml = etree.parse(StringIO(file.read()))
    file.close()
    xpath = xml.xpath(f'/Modules/ModuleGroup[@index = "{moduleGroupIndex}"]/Module')
    for module in xpath:
      moduleobj = Module(module.attrib['index'], module.attrib['name'], moduleGroup)
      modules.append(moduleobj)
    return modules
    
  def __init__(self, index: int, name: str, moduleGroup: 'ModuleGroup', submodules: list[Submodule] = []):
    self.__index = index
    self.__name = name
    self.__module_group = moduleGroup
    self.__submodules = submodules

  def addSubmodules(self):
    submodules = Submodule.getSubmodules(self)
    self.__submodules = submodules

  def getIndex(self):
    return self.__index
  
  def getModuleGroupIndex(self):
    return self.__module_group.getIndex()

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
    
  def __init__(self, index: int, name: str, modules: list[Module] = []):
    self.__index = index
    self.__name = name
    self.__modules = modules

  def addModules(self):
    modules = Module.getModules(self)
    self.__modules = modules

  def getIndex(self):
    return self.__index