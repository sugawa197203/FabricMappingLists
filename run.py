import sys
import os
import re
import tqdm

directry = sys.argv[1]
classMapping = dict()
methodMapping = dict()
fieldMapping = dict()

classPattern = r'CLASS net/minecraft/class_([0-9]+) net/minecraft/(\S+)'
fieldPattern = r'\tFIELD field_([0-9]+) (\S+)'
methodPattern = r'\tMETHOD method_([0-9]+) (\S+)'

def get_files(serchDirectry, files = []):
	for filePath in os.listdir(serchDirectry):
		if os.path.isdir(serchDirectry + '/' + filePath):
			get_files(serchDirectry + '/' + filePath, files)
		else:
			if filePath.endswith('.mapping'):
				files.append(serchDirectry + '/' + filePath)
	return files

def analysis(fileName, classMapping = classMapping, methodMapping = methodMapping, fieldMapping = fieldMapping):
	classFlag = False
	with open(fileName, 'r', encoding='utf-8') as file:
		for line in file:
			if re.match(classPattern, line):
				if classFlag:
					assert False, 'classFlag'
				classFlag = True

				t = re.match(classPattern, line).group()
				t = t.split(' ')
				key = t[1].split('/')[-1]
				value = ".".join(t[2].split('/')[2:])
				classMapping[key] = value
				return
			
			if re.match(fieldPattern, line):
				t = re.match(fieldPattern, line).group()
				t = t.split(' ')
				key = t[1]
				value = t[2]
				fieldMapping[key] = value
			
			if re.match(methodPattern, line):
				t = re.match(methodPattern, line).group()
				t = t.split(' ')
				key = t[1]
				value = t[2]
				methodMapping[key] = value

print(directry)
files = get_files(directry)	

for file in tqdm.tqdm(files):
	analysis(file, classMapping, methodMapping, fieldMapping)

with open('class.csv', 'w', encoding='utf-8') as file:
	for key, value in classMapping.items():
		file.write(key + ',' + value + '\n')

with open('method.csv', 'w', encoding='utf-8') as file:
	for key, value in methodMapping.items():
		file.write(key + ',' + value + '\n')

with open('field.csv', 'w', encoding='utf-8') as file:
	for key, value in fieldMapping.items():
		file.write(key + ',' + value + '\n')
