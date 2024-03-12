import sys
import os

src = sys.args[1]

classMappingCSV = sys.args[2]
fieldMappingCSV = sys.args[3]
methodMappingCSV = sys.args[4]

classMapping = dict()
fieldMapping = dict()
methodMapping = dict()

javaFiles = []

def initMapping(classCSV, fieldCSV, methodCSV):
	with open(classCSV, 'r', encoding='utf-8') as file:
		for line in file:
			line = line.split(',')
			classMapping[line[0]] = line[1]
	
	with open(fieldCSV, 'r', encoding='utf-8') as file:
		for line in file:
			line = line.split(',')
			fieldMapping[line[0]] = line[1]
	
	with open(methodCSV, 'r', encoding='utf-8') as file:
		for line in file:
			line = line.split(',')
			methodMapping[line[0]] = line[1]

def get_files(serchDirectry, files = []):
	for filePath in os.listdir(serchDirectry):
		if os.path.isdir(serchDirectry + '/' + filePath):
			get_files(serchDirectry + '/' + filePath, files)
		else:
			if filePath.endswith('.java'):
				files.append(serchDirectry + '/' + filePath)
	return files


def codeReplace(file, mapping:dict):
	keys = mapping.keys()
	javaCode = ''
	with open(file, 'r', encoding='utf-8') as f:
		javaCode = f.read()
	
	for key in keys:
		javaCode = javaCode.replace(key, mapping[key])
	
	with open(file, 'w', encoding='utf-8') as f:
		f.write(javaCode)

initMapping(classMappingCSV, fieldMappingCSV, methodMappingCSV)
javaFiles = get_files(src)

for file in javaFiles:
	codeReplace(file, classMapping)
	codeReplace(file, fieldMapping)
	codeReplace(file, methodMapping)
