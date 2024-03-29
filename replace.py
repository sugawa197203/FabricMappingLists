import sys
import os
import tqdm
import re

src = sys.argv[1]

classMappingCSV = sys.argv[2]
fieldMappingCSV = sys.argv[3]
methodMappingCSV = sys.argv[4]

classMapping = dict()
fieldMapping = dict()
methodMapping = dict()

javaFiles = []

def initMapping(classCSV, fieldCSV, methodCSV):
	with open(classCSV, 'r', encoding='utf-8') as file:
		for line in file:
			line = line.split(',')
			classMapping[line[0]] = line[1].strip()

	with open(fieldCSV, 'r', encoding='utf-8') as file:
		for line in file:
			line = line.split(',')
			fieldMapping[line[0]] = line[1].strip()

	with open(methodCSV, 'r', encoding='utf-8') as file:
		for line in file:
			line = line.split(',')
			methodMapping[line[0]] = line[1].strip()

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
		if re.search(key + r'[^0-9]', javaCode):
			print(key)
			javaCode = javaCode.replace(key, mapping[key])

	with open(file, 'w', encoding='utf-8') as f:
		f.write(javaCode)

def classReplace(file, mapping:dict):
	keys = mapping.keys()
	javaCode = ''
	replacedJavaCode = ''
	with open(file, 'r', encoding='utf-8') as f:
		javaCode = f.read()

	for line in javaCode.split('\n'):
		for key in keys:
			pattern = key + '[^0-9]'
			if 'import' in line:
				if re.search(pattern, line):
					line = re.sub(key, mapping[key], line)
			elif re.search(pattern, line):
				line = re.sub(key, mapping[key].split(".")[-1], line)
		replacedJavaCode += line + '\n'

	with open(file, 'w', encoding='utf-8') as f:
		f.write(replacedJavaCode)

initMapping(classMappingCSV, fieldMappingCSV, methodMappingCSV)
javaFiles = get_files(src)

for file in tqdm.tqdm(javaFiles):
	classReplace(file, classMapping)
	codeReplace(file, fieldMapping)
	codeReplace(file, methodMapping)
