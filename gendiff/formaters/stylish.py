TAB = 2


def format_value(value, lvl=1):
    if value in [True, False]:
        return str(value).lower()
    elif value is None:
        return 'null'
    elif isinstance(value, dict):
        answer = unpack_dict(value, lvl)
        return answer
    else:
        return value


def unpack_dict(d, lvl=1):
    tab = TAB * 2 * ' '
    answer = '{\n'
    for key, val in d.items():
        if isinstance(val, dict) and lvl == 1:
            lvl += 1
            answer += f"{(lvl) * tab}{key}: {unpack_dict(val, lvl+1)}"
        elif isinstance(val, dict):
            answer += f"{(lvl) * tab}{key}: {unpack_dict(val, lvl+1)}"
        elif lvl == 1:
            answer += f"{(lvl+1) * tab}{key}: {val}"
        else:
            answer += f"{lvl * tab}{key}: {val}"
        answer += "\n"
    answer += f"{(lvl-1) * tab}" + "}"
    return answer


def get_answer_str(diff_tree, lvl=1):
    tab = TAB * " "
    answer = '{\n'
    for child in diff_tree:
        if child['status'] == 'removed':
            answer += f"{lvl * tab}- {child['key']}: " \
                      f"{format_value(child['value'], lvl)}"
            answer += '\n'

        if child['status'] == 'added':
            answer += f"{lvl * tab}+ {child['key']}: " \
                      f"{format_value(child['value'], lvl)}"
            answer += '\n'

        if child['status'] == 'changed':
            answer += f"{lvl * tab}- {child['key']}: "
            answer += f"{format_value(child['old_value'], lvl)}"
            answer += '\n'
            answer += f"{lvl * tab}+ {child['key']}: "
            answer += f"{format_value(child['new_value'], lvl)}"
            answer += '\n'

        if child['status'] == 'nested':
            answer += f"{lvl * tab}  {child['key']}: "
            answer += get_answer_str(child['value'], lvl + 2)
            answer += '\n'

        if child['status'] == 'unchanged':
            answer += f"{lvl * tab}  {child['key']}: "
            answer += f"{format_value(child['value'], lvl)}"
            answer += '\n'
    if lvl == 1:
        answer += '}'
    else:
        answer += f"{(lvl - 1) * tab}" + '}'
    return answer


def format_stylish(diff_tree):
    return get_answer_str(diff_tree)
