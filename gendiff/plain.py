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
            key = i['path']
            if i['path'] not in keys and i['sign'] != " ":
                if isinstance(i['value'], dict):
                    keys[key] = [COMPLEX]
                else:
                    keys[key] = [i['value']]
            elif i['path'] in keys:
                if isinstance(i['value'], dict):
                    keys[key].append(COMPLEX)
                else:
                    keys[key].append(i['value'])
    updated = {}
    for key in keys:
        if len(keys[key]) == 2:
            updated[key] = keys[key]
    print(updated)
    return updated


def make_answer(new_tree, ud, diff_tree, answer=''):
    tree = copy.deepcopy(diff_tree)
    for i in tree:
        if i['value'] not in ['true', 'false', 'null', '[complex value]'] \
                and isinstance(i['value'], str):
            i["value"] = '\'' + i['value'] + '\''
        if isinstance(i['value'], dict):
            i['value'] = COMPLEX
        if i['sign'] == '-' and i['path'] not in ud:
            answer += f"{PRO} '{i['path']}' {REMOVE}"
            answer += "\n"
        elif i['sign'] == '+' and i['path'] not in ud:
            answer += f"{PRO} '{i['path']}' {ADDED}{i['value']}"
            answer += "\n"
        elif i['sign'] == '+' and i['path'] in ud:
            key = i['path']
            if ud[key][0] not in ['true', 'false', 'null', '[complex value]'] \
                    and isinstance(ud[key][0], str):
                ud[key][0] = '\'' + ud[key][0] + '\''
            if ud[key][1] not in ['true', 'false', 'null', '[complex value]'] \
                    and isinstance(ud[key][1], str):
                ud[key][1] = '\'' + ud[key][1] + '\''

            answer += f"{PRO} '{i['path']}' {UPDATE}{ud[key][0]} to " \
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
