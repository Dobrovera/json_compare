#!/usr/bin/env python3


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
                keys[key] = [i['value']]
            elif i["key"] in keys:
                keys[key].append(i['value'])
    updated = {}
    for key in keys:
        if len(keys[key]) == 2:
            updated[key] = keys[key]
    return updated


def make_answer(new_tree, ud, diff_tree, answer=''):
    for i in diff_tree:
        if isinstance(i['value'], dict):
            i['value'] = complex
        if i['sign'] == '-' and i['key'] not in ud:
            answer += f"{pro} '{i['path']}' {remove}"
            answer += "\n"
        elif i['sign'] == '+' and i['key'] not in ud:
            answer += f"{pro} '{i['path']}' {added}'{i['value']}'"
            answer += "\n"
        elif i['sign'] == '+' and i['key'] in ud:
            key = i['key']
            answer += f"{pro} '{i['path']}' {update}'{ud[key][0]}' to " \
                      f"'{ud[key][1]}'"
            answer += "\n"
        elif i['sign'] == ' ':
            if isinstance(i['value'], list):
                answer = make_answer(new_tree=new_tree, ud=ud,
                                     diff_tree=i['value'], answer=answer)
        elif i['sign'] == "+" and i['key'] not in ud:
            if isinstance(i['value'], dict):
                answer += f"{pro} '{i['path']}' {added}{complex}"
    return answer


def plain(diff_tree):
    new_tree = diff_tree_path(diff_tree)
    ud = new_dict_updated(new_tree)
    answer = make_answer(new_tree, ud, diff_tree)
    return answer
