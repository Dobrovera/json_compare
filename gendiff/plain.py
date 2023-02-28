#!/usr/bin/env python3
import copy

added = "was added with value: "
remove = "was removed"
update = "was updated. From "
pro = "Property"
complex = "[complex value]"


def diff_tree_path(diff_tree, curr_path=''):
    for i in diff_tree:
        path = curr_path + f"{i['key']}"
        i['path'] = path
        if isinstance(i["value"], list):
            path += "."
            for n in i['value']:
                if isinstance(n['value'], list):
                    new_path = path + n['key'] + '.'
                    diff_tree_path(n['value'], curr_path=new_path)
                else:
                    new_path = path + n['key']
                    n['path'] = new_path
    return diff_tree


def new_dict_updated(diff_tree, keys={}):
    for i in diff_tree:
        if i['value'] is True:
            i['value'] = 'true'
        elif i['value'] is False:
            i['value'] = 'false'
        elif i['value'] is None:
            i['value'] = 'null'
        if isinstance(i['value'], list):
            child = i['value']
            new_dict_updated(child, keys)
        else:
            key = i['key']
            if i["key"] not in keys and i['sign'] != " ":
                if isinstance(i['value'], dict):
                    keys[key] = [complex]
                else:
                    keys[key] = [i['value']]
            elif i["key"] in keys:
                if isinstance(i['value'], dict):
                    keys[key].append(complex)
                else:
                    keys[key].append(i['value'])
    updated = {}
    for key in keys:
        if len(keys[key]) == 2:
            updated[key] = keys[key]
    return updated


def make_answer(new_tree, ud, diff_tree, answer=''):
    tree = copy.deepcopy(diff_tree)
    for i in tree:
        if i['value'] not in ['true', 'false', 'null', '[complex value]'] \
                and isinstance(i['value'], str):
            i["value"] = '\'' + i['value'] + '\''
        if isinstance(i['value'], dict):
            i['value'] = complex
        if i['sign'] == '-' and i['key'] not in ud:
            answer += f"{pro} '{i['path']}' {remove}"
            answer += "\n"
        elif i['sign'] == '+' and i['key'] not in ud:
            answer += f"{pro} '{i['path']}' {added}{i['value']}"
            answer += "\n"
        elif i['sign'] == '+' and i['key'] in ud:
            key = i['key']
            if ud[key][0] not in ['true', 'false', 'null', '[complex value]'] \
                    and isinstance(ud[key][0], str):
                ud[key][0] = '\'' + ud[key][0] + '\''
            if ud[key][1] not in ['true', 'false', 'null', '[complex value]'] \
                    and isinstance(ud[key][1], str):
                ud[key][1] = '\'' + ud[key][1] + '\''

            answer += f"{pro} '{i['path']}' {update}{ud[key][0]} to " \
                      f"{ud[key][1]}"
            answer += "\n"
        elif i['sign'] == ' ':
            if isinstance(i['value'], list):
                answer = make_answer(new_tree=new_tree, ud=ud,
                                     diff_tree=i['value'], answer=answer)
    return answer


def plain(diff_tree):
    new_tree = diff_tree_path(diff_tree)
    ud = new_dict_updated(new_tree)
    answer = make_answer(new_tree, ud, diff_tree)
    return answer
