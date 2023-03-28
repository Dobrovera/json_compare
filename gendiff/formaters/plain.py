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


def make_answer(diff_tree_with_path, answer='', curr_path=''):
    for node in diff_tree_with_path:
        if node['status'] == 'removed':
            answer += f"{PRO} '{curr_path + node['key']}' {REMOVE}"
            answer += "\n"
        elif node['status'] == 'added':
            answer += f"{PRO} '{curr_path + node['key']}' {ADDED}" \
                      f"{format_value(node['value'])}"
            answer += "\n"
        elif node['status'] == 'changed':
            answer += f"{PRO} '{curr_path + node['key']}' {UPDATE}" \
                      f"{format_value(node['old_value'])}" \
                      f" to {format_value(node['new_value'])}"
            answer += "\n"
        elif node['status'] == 'nested':
            answer = make_answer(diff_tree_with_path=node['value'],
                                 answer=answer,
                                 curr_path=curr_path + node['key'] + '.')
    return answer


def plain(diff_tree):
    answer = make_answer(diff_tree)
    return answer.rstrip()
