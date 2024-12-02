from lxml import etree
import json

def displayModules():
  output = []
  file = open('data/modules.xml', encoding = 'utf-8')
  modules = etree.fromstring(file.read())
  for moduleGroup in modules.iter('ModuleGroup'):
    moduleGroupName = moduleGroup.attrib['name']
    moduleGroupIndex = moduleGroup.attrib['index']
    moduleGroupChilds = []
    for module in moduleGroup.iter('Module'):
      moduleName = module.attrib['name']
      moduleIndex = module.attrib['index']
      moduleChilds = []
      for submodule in module.iter('Submodule'):
        submoduleName = submodule.attrib['name']
        submoduleIndex = submodule.attrib['index']
        moduleChilds.append({
          'index': f'{moduleGroupIndex}.{moduleIndex}.{submoduleIndex}',
          'name': submoduleName
        })
      moduleGroupChilds.append({
        'index': f'{moduleGroupIndex}.{moduleIndex}',
        'name': moduleName,
        'submodules': moduleChilds
      })
    output.append({
      'index': f'{moduleGroupIndex}',
      'name': moduleGroupName,
      'modules': moduleGroupChilds
    })
  return output


with open('output.json', 'w', encoding = 'utf-8') as file:
  file.write(json.dumps(displayModules(), ensure_ascii = False, indent = 2))