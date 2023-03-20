import copy

ADDED = "was added with value: "
REMOVE = "was removed"
UPDATE = "was updated. From "
PRO = "Property"
COMPLEX = "[complex value]"


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


def new_dict_updated(diff_tree, keys=None):
    if keys is None:
        keys = {}
    for i in diff_tree:
        if i['status'] == 'nested':
            child = i['value']
            new_dict_updated(child, keys)
        else:
            key = i['path']
            if i['path'] not in keys and i['status'] == 'changed':
                if isinstance(i['value'], dict) \
                        and type(i['value_2']) is not dict:
                    keys[key] = [COMPLEX, i['value_2']]
                elif isinstance(i['value_2'], dict) \
                        and type(i['value']) is not dict:
                    keys[key] = [i['value'], COMPLEX]
                else:
                    keys[key] = [i['value'], i['value_2']]
    updated = {}
    for key in keys:
        if len(keys[key]) == 2:
            updated[key] = keys[key]
    for keys in updated:
        values_list = []
        for value in updated[keys]:
            if value is True:
                values_list.append('true')
            elif value is False:
                values_list.append('false')
            elif value is None:
                values_list.append('null')
            else:
                values_list.append(value)
        updated[keys] = values_list
    return updated


def make_answer(new_tree, ud, diff_tree, answer=''):
    tree = copy.deepcopy(diff_tree)
    for i in tree:
        if i['value'] is True:
            i['value'] = 'true'
        elif i['value'] is False:
            i['value'] = 'false'
        elif i['value'] is None:
            i['value'] = 'null'
        if isinstance(i['value'], dict):
            i['value'] = COMPLEX
        if i['status'] == 'removed':
            answer += f"{PRO} '{i['path']}' {REMOVE}"
            answer += "\n"
        elif i['status'] == 'added':
            if i['value'] in ['true', 'false', 'null', '[complex value]']:
                answer += f"{PRO} '{i['path']}' {ADDED}{i['value']}"
                answer += "\n"
            else:
                answer += f"{PRO} '{i['path']}' {ADDED}'{i['value']}'"
                answer += "\n"
        elif i['status'] == 'changed':
            key = i['path']
            if ud[key][0] not in ['true', 'false', 'null', '[complex value]'] \
                    and isinstance(ud[key][0], str):
                ud[key][0] = '\'' + ud[key][0] + '\''
            if ud[key][1] not in ['true', 'false', 'null', '[complex value]'] \
                    and isinstance(ud[key][1], str):
                ud[key][1] = '\'' + ud[key][1] + '\''
            if i['value'] is True:
                i['value'] = 'true'
            elif i['value'] is False:
                i['value'] = 'false'
            elif i['value'] is None:
                i['value'] = 'null'
            answer += f"{PRO} '{i['path']}' {UPDATE}{ud[key][0]} to " \
                      f"{ud[key][1]}"
            answer += "\n"
        elif i['status'] == 'nested':
            if isinstance(i['value'], list):
                answer = make_answer(new_tree=new_tree, ud=ud,
                                     diff_tree=i['value'], answer=answer)
    return answer


def plain(diff_tree):
    new_tree = diff_tree_path(diff_tree)
    ud = new_dict_updated(new_tree)
    answer = make_answer(new_tree, ud, diff_tree)
    return answer.rstrip()
