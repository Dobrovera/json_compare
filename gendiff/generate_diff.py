import json
import yaml
import os
from gendiff.formaters.stylish import stylish
from gendiff.formaters.plain import plain
from gendiff.formaters.json import f_json


def parse(data, format):
    if format == ".json":
        return json.load(data)
    elif format == ".yml" or format == ".yaml":
        return yaml.safe_load(data)


def get_data(file_path):
    name, format = os.path.splitext(os.path.normpath(file_path))
    with open(file_path) as file:
        return parse(file, format)


def build_tree_structure(files, file_1, file_2):
    diff_tree = []
    for key in files:
        # Проверяем все ключи из объединенного списка
        if key in file_1 and key not in file_2:
            # Если ключ есть только в первом файле
            diff_tree.append({
                "key": key,
                "status": 'removed',
                "value": file_1[key],
            })
        elif key in file_2 and key not in file_1:
            # Если ключ есть только во втором файле
            diff_tree.append({
                "key": key,
                "status": 'added',
                "value": file_2[key]
            })
        elif key in file_1 and key in file_2:
            # Если ключ в обоих файлах
            if isinstance(file_1[key], dict) and isinstance(file_2[key], dict):
                # Если значения по ключу словари
                fls = sorted(list(set(file_1[key]) | set(file_2[key])))
                result = build_tree_structure(fls, file_1[key], file_2[key])
                diff_tree.append({
                    "key": key,
                    "status": 'nested',
                    "value": result
                })

            elif file_1[key] == file_2[key]:
                # Значения не словари и значения равны
                diff_tree.append({
                    "key": key,
                    "status": 'unchanged',
                    "value": file_1[key]
                })
            else:
                # Если значения не равны
                diff_tree.append({
                    "key": key,
                    "status": 'changed',
                    "value": file_1[key],
                    "value_2": file_2[key]
                })
    return diff_tree


def generate_diff(file_path1, file_path2, format_name='stylish'):
    files = sorted(list(set(get_data(file_path1).keys())
                        | set(get_data(file_path2).keys())))
    file_1 = dict(sorted(get_data(file_path1).items()))
    file_2 = dict(sorted(get_data(file_path2).items()))
    result = build_tree_structure(files, file_1, file_2)
    if format_name == 'stylish':
        return stylish(result)
    elif format_name == "plain":
        return plain(result)
    elif format_name == 'json':
        return f_json(result)
