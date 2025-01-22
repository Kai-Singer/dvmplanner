from dvmplanner.scripts.main import BASE_DIR
from lxml import etree
from io import StringIO

def getXml():
  path = BASE_DIR + '/data/modules.xml'
  file = open(path, 'r', encoding = 'utf-8')
  xml = etree.parse(StringIO(file.read()))
  file.close()
  return xml

def saveXml(xml):
  path = BASE_DIR + '/data/modules.xml'
  xmlData = etree.tostring(xml, pretty_print = True, encoding = 'utf-8').decode()
  file = open(path, 'w', encoding = 'utf-8')
  file.write(xmlData)
  file.close()

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
    xml = getXml()
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
  
  def getModule(self):
    return self.__module
  
  def getModuleGroup(self):
    return self.__module.getModuleGroup()
  
  def getData(self, keyName: str):
    data = {
      'index': self.__index,
      'name': self.__name,
      'semester': self.__semester,
      'module': self.__module
    }
    return data[keyName]
  
  def remove(self):
    xml = getXml()
    element = xml.xpath(f'/Modules/ModuleGroup[@index = "{ self.getModuleGroup().getIndex() }"]/Module[@index = "{ self.__module.getIndex() }"]/Submodule[@index = "{ self.__index }"]')[0]
    parent = element.getparent()
    parent.remove(element)
    saveXml(xml)

  def addToXml(self):
    xml = getXml()
    element = etree.Element('Submodule', index = self.__index, name = self.__name, semester = self.__semester)
    parent = xml.xpath(f'/Modules/ModuleGroup[@index = "{ self.getModuleGroup().getIndex() }"]/Module[@index = "{ self.__module.getIndex() }"]')[0]
    children = parent.getchildren()
    for child in children:
      parent.remove(child)
    children.append(element)
    sortedChildren = sorted(children, key = lambda x: x.attrib['index'])
    for child in sortedChildren:
      parent.append(child)
    saveXml(xml)

  def edit(self, name, semester):
    xml = getXml()
    element = xml.xpath(f'/Modules/ModuleGroup[@index = "{ self.getModuleGroup().getIndex() }"]/Module[@index = "{ self.__module.getIndex() }"]/Submodule[@index = "{ self.__index }"]')[0]
    element.attrib['name'] = name
    element.attrib['semester'] = semester
    saveXml(xml)


class Module:
  @staticmethod
  def getModules(moduleGroup: 'ModuleGroup'):
    moduleGroupIndex = moduleGroup.getIndex()
    modules = []
    xml = getXml()
    xpath = xml.xpath(f'/Modules/ModuleGroup[@index = "{ moduleGroupIndex }"]/Module')
    for module in xpath:
      moduleobj = Module(module.attrib['index'], module.attrib['name'], moduleGroup)
      modules.append(moduleobj)
    return modules
  
  @staticmethod
  def getByIndex(index: str):
    indexSplit = index.split('.')
    result = None
    for moduleGroup in ModuleGroup.getModuleGroups():
      if moduleGroup.getIndex() == indexSplit[0]:
        for module in Module.getModules(moduleGroup):
          if module.getIndex() == indexSplit[1]:
            result = module
    return result
    
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
  
  def getModuleGroup(self):
    return self.__module_group
  
  def getData(self, keyName: str):
    data = {
      'index': self.__index,
      'name': self.__name,
      'module_group': self.__module_group,
      'submodules': self.__submodules
    }
    return data[keyName]
  
  def remove(self):
    xml = getXml()
    element = xml.xpath(f'/Modules/ModuleGroup[@index = "{ self.__module_group.getIndex() }"]/Module[@index = "{ self.__index }"]')[0]
    parent = element.getparent()
    parent.remove(element)
    saveXml(xml)

  def addToXml(self):
    xml = getXml()
    element = etree.Element('Module', index = self.__index, name = self.__name)
    parent = xml.xpath(f'/Modules/ModuleGroup[@index = "{ self.__module_group.getIndex() }"]')[0]
    children = parent.getchildren()
    for child in children:
      parent.remove(child)
    children.append(element)
    sortedChildren = sorted(children, key = lambda x: x.attrib['index'])
    for child in sortedChildren:
      parent.append(child)
    saveXml(xml)

  def edit(self, name):
    xml = getXml()
    element = xml.xpath(f'/Modules/ModuleGroup[@index = "{ self.__module_group.getIndex() }"]/Module[@index = "{ self.__index }"]')[0]
    element.attrib['name'] = name
    saveXml(xml)

class ModuleGroup:
  @staticmethod
  def getModuleGroups():
    moduleGroups = []
    xml = getXml()
    xpath = xml.xpath('/Modules/ModuleGroup')
    for moduleGroup in xpath:
      modulegroupobj = ModuleGroup(moduleGroup.attrib['index'], moduleGroup.attrib['name'])
      moduleGroups.append(modulegroupobj)
    return moduleGroups
  
  @staticmethod
  def getByIndex(index: str):
    result = None
    for moduleGroup in ModuleGroup.getModuleGroups():
      if moduleGroup.getIndex() == index:
        result = moduleGroup
    return result
    
  def __init__(self, index: int, name: str):
    self.__index = index
    self.__name = name
    self.__modules = Module.getModules(self)

  def getIndex(self):
    return self.__index
  
  def getCompleteIndex(self):
    return self.getIndex()
  
  def getData(self, keyName: str):
    data = {
      'index': self.__index,
      'name': self.__name,
      'modules': self.__modules
    }
    return data[keyName]
  
  def remove(self):
    xml = getXml()
    element = xml.xpath(f'/Modules/ModuleGroup[@index = "{ self.__index }"]')[0]
    parent = element.getparent()
    parent.remove(element)
    saveXml(xml)

  def addToXml(self):
    xml = getXml()
    element = etree.Element('ModuleGroup', index = self.__index, name = self.__name)
    parent = xml.xpath(f'/Modules')[0]
    children = parent.getchildren()
    for child in children:
      parent.remove(child)
    children.append(element)
    sortedChildren = sorted(children, key = lambda x: x.attrib['index'])
    for child in sortedChildren:
      parent.append(child)
    saveXml(xml)
  
  def edit(self, name):
    xml = getXml()
    element = xml.xpath(f'/Modules/ModuleGroup[@index = "{ self.__index }"]')[0]
    element.attrib['name'] = name
    saveXml(xml)