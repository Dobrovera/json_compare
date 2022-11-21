#!/usr/bin/env python3


import json
import os


def parse(data, format):
	if format == ".json":
		return json.load(data)


def get_data(file_path):
	name, format = os.path.splitext(os.path.normpath(file_path))
	with open(file_path) as file:
		return parse(file, format)


def difference_tree(file_path1, file_path2):
	files = sorted(list(set(get_data(file_path1).keys()) | set(get_data(file_path2).keys())))
	file_1 = dict(sorted(get_data(file_path1).items()))
	file_2 = dict(sorted(get_data(file_path2).items()))
	in_first_file = "- "
	in_second_file = "+ "
	space = "  "
	diff_tree = []
	for key in files:
	#Проверяем все ключи из объединенного списка
		if key in file_1 and key in file_2:
		#Если ключ в обоих файлах
			if file_1[key] == file_2[key]:
			#И значения равны
				diff_tree.append({
					"key": key,
					"sign": space,
					"value": file_1[key]
				})
			else:
			#Если значения не равны
				diff_tree.append({
					"key": key,
					"sign": in_first_file,
					"value": file_1[key]
				})
				diff_tree.append({
					"key": key,
					"sign": in_second_file,
					"value": file_2[key]
				})
		if key in file_1 and key not in file_2:
		#Если ключ есть только в первом файле
			diff_tree.append({
				"key": key,
				"sign": in_first_file,
				"value": file_1[key]
			})
		elif key in file_2 and key not in file_1:
		#Если ключ есть только во втором файле
			diff_tree.append({
				"key": key,
				"sign": in_second_file,
				"value": file_2[key]
			})
	return diff_tree


def unpacking(diff_tree):
	line_break = "\n"
	answer = '{ \n'
	for child in diff_tree:
		if child['value'] == True:
			child['value'] = 'true'
		elif child['value'] == False:
			child['value'] = 'false'
		answer += f"  {child['sign']} {child['key']}: {child['value']}"
		answer += '\n'
	answer += '}'
	return answer


def generate_diff(file_path1, file_path2):
	print(unpacking(difference_tree(file_path1, file_path2)))


# if __name__ == '__main__':
# 	generate_diff('/home/vera/python-project-50/files/file1.json', '/home/vera/python-project-50/files/file2.json')