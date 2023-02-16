#!/usr/bin/env python3


import json
import yaml
import os


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


def unpack_dict(d, base_tab, lvl=1):
    tab = '    '
    answer = '{\n'
    for key, val in d.items():
        if isinstance(val, dict):
            if lvl == 1:
                lvl += 1
                r = f"{(lvl) * tab}{key}: {unpack_dict(val, lvl*tab, lvl+1)}"
            else:
                r = f"{(lvl) * tab}{key}: {unpack_dict(val, lvl*tab, lvl+1)}"
            answer += r
        else:
            if lvl == 1:
                answer += f"{(lvl+1) * tab}{key}: {val}"
            else:
                answer += f"{lvl * tab}{key}: {val}"
        answer += "\n"
    answer += f"{(lvl-1) * tab}" + "}"
    return answer


def unpacking(diff_tree, lvl=1):
    tab = "  "
    answer = '{\n'
    for child in diff_tree:
        if child['value'] is True:
            child['value'] = 'true'
        elif child['value'] is False:
            child['value'] = 'false'
        if isinstance(child['value'], list):
            answer += f"{lvl * tab}{child['sign']} {child['key']}: "
            answer += unpacking(child['value'], lvl+2)
            answer += '\n'
        elif isinstance(child["value"], dict):
            # answer += "{\n"
            answer += f"{lvl * tab}{child['sign']} {child['key']}: "
            r = unpack_dict(child['value'], lvl*tab, lvl)
            # r = json.dumps(child['value'], sort_keys=True, indent=4)
            answer += r
            answer += '\n'
        else:
            answer += f"{lvl * tab}{child['sign']} {child['key']}: " \
                      f"{child['value']}"
            answer += '\n'
    if lvl == 1:
        answer += '}'
    else:
        answer += f"{(lvl-1) * tab}" + '}'
    return answer


def generate_diff(file_path1, file_path2):
    result = difference_tree(file_path1, file_path2)
    return unpacking(result)
