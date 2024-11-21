from lxml import etree

def displayModules():
  output = {}
  file = open('data/modules.xml', encoding = 'utf-8')
  modules = etree.fromstring(file.read())
  for modulegroup in modules.iter('ModuleGroup'):
    modulegroup.attrib['name']

print(displayModules())