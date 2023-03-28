import copy

ADDED = "was added with value: "
REMOVE = "was removed"
UPDATE = "was updated. From "
PRO = "Property"
COMPLEX = "[complex value]"


def format_value(value):
    if value in [True, False]:
        return str(value).lower()
    elif value is None:
        return 'null'
    elif isinstance(value, dict):
        return COMPLEX
    else:
        return f"'{value}'"


def diff_tree_path(diff_tree_with_path, curr_path=''):
    for node in diff_tree_with_path:
        path = curr_path + f"{node['key']}"
        node['path'] = path
        if node["status"] == 'nested':
            path += "."
            for n in node['value']:
                if n["status"] == 'nested':
                    new_path = path + n['key'] + '.'
                    diff_tree_path(n['value'], curr_path=new_path)
                else:
                    new_path = path + n['key']
                    n['path'] = new_path
    return diff_tree_with_path


def make_answer(diff_tree_with_path, answer=''):
    for node in diff_tree_with_path:
        if node['status'] == 'removed':
            answer += f"{PRO} '{node['path']}' {REMOVE}"
            answer += "\n"
        elif node['status'] == 'added':
            answer += f"{PRO} '{node['path']}' {ADDED}" \
                      f"{format_value(node['value'])}"
            answer += "\n"
        elif node['status'] == 'changed':
            answer += f"{PRO} '{node['path']}' {UPDATE}" \
                      f"{format_value(node['value'])}" \
                      f" to {format_value(node['value_2'])}"
            answer += "\n"
        elif node['status'] == 'nested':
            answer = make_answer(diff_tree_with_path=node['value'],
                                 answer=answer)
    return answer


def plain(diff_tree):
    # Для неизменности diff_tree
    diff_tree_with_path = copy.deepcopy(diff_tree)
    new_tree = diff_tree_path(diff_tree_with_path)
    answer = make_answer(new_tree)
    return answer.rstrip()
