from lxml import etree

def displayModules():
  output = {}
  file = open('data/modules.xml', encoding = 'utf-8')
  modules = etree.fromstring(file.read())
  for modulegroup in modules.iter('ModuleGroup'):
    output[modulegroup.attrib['name']] = {}
    for module in modulegroup.iter('Module'):
      output[modulegroup.attrib['name']][module.attrib['name']] = []
      for submodule in module.iter('Submodule'):
        output[modulegroup.attrib['name']][module.attrib['name']].append(submodule.attrib['name'])
  return output

print(displayModules())