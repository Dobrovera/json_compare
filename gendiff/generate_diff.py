#!/usr/bin/env python3


import json
import yaml
import os
from gendiff.stylish import slylish
from gendiff.plain import plain
from gendiff.json import f_json


def parse(data, format):
    if format == ".json":
        return json.load(data)
    elif format == ".yml" or format == ".yaml":
        return yaml.safe_load(data)


def get_data(file_path):
    name, format = os.path.splitext(os.path.normpath(file_path))
    with open(file_path) as file:
        return parse(file, format)


def do_things(files, file_1, file_2):
    in_first_file = "-"
    in_second_file = "+"
    space = " "
    diff_tree = []
    for key in files:
        # Проверяем все ключи из объединенного списка
        if key in file_1 and key not in file_2:
            # Если ключ есть только в первом файле
            diff_tree.append({
                "key": key,
                "sign": in_first_file,
                "value": file_1[key],
            })
        elif key in file_2 and key not in file_1:
            # Если ключ есть только во втором файле
            diff_tree.append({
                "key": key,
                "sign": in_second_file,
                "value": file_2[key]
            })
        elif key in file_1 and key in file_2:
            # Если ключ в обоих файлах
            value1 = file_1[key]
            value2 = file_2[key]
            if isinstance(value1, dict) and isinstance(value2, dict):
                # Если значения по ключу словари
                f_1 = value1
                f_2 = value2
                fls = sorted(list(set(f_1) | set(f_2)))
                result = do_things(fls, f_1, f_2)
                diff_tree.append({
                    "key": key,
                    "sign": space,
                    "value": result
                })

            else:
                if file_1[key] == file_2[key]:
                    # Значения не словари и значения равны
                    diff_tree.append({
                        "key": key,
                        "sign": space,
                        "value": file_1[key]
                    })
                else:
                    # Если значения не равны
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
    return diff_tree


def difference_tree(file_path1, file_path2):
    files = sorted(list(set(get_data(file_path1).keys()) |
                        set(get_data(file_path2).keys())))
    file_1 = dict(sorted(get_data(file_path1).items()))
    file_2 = dict(sorted(get_data(file_path2).items()))
    return do_things(files, file_1, file_2)


def generate_diff(file_path1, file_path2, format_name='stylish'):
    result = difference_tree(file_path1, file_path2)
    if format_name == 'stylish':
        return slylish(result)
    elif format_name == "plain":
        return plain(result)
    elif format_name == 'json':
        return f_json(result)
