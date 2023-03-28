TAB = 2


def format_value(value):
    if value in [True, False]:
        return str(value).lower()
    elif value is None:
        return 'null'
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
        # Если ключ был удален И содержит словарь
        if child['status'] == 'removed' and type(child['value']) is dict:
            answer += f"{lvl * tab}- {child['key']}: "
            answer += unpack_dict(child['value'], lvl)
            answer += '\n'
        elif child['status'] == 'removed':
            answer += f"{lvl * tab}- {child['key']}: " \
                      f"{format_value(child['value'])}"
            answer += '\n'

        # Если ключ был добавлен во второй файл И содержит словарь
        if child['status'] == 'added' and type(child['value']) is dict:
            answer += f"{lvl * tab}+ {child['key']}: "
            answer += unpack_dict(child['value'], lvl)
            answer += '\n'
        elif child['status'] == 'added':
            answer += f"{lvl * tab}+ {child['key']}: " \
                      f"{format_value(child['value'])}"
            answer += '\n'

        # Если ключ поменялся
        if child['status'] == 'changed':
            # И содержит словарь в первом файле
            if type(child['value']) is dict:
                answer += f"{lvl * tab}- {child['key']}: "
                answer += unpack_dict(child['value'], lvl)
                answer += '\n'
                answer += f"{lvl * tab}+ {child['key']}: " \
                          f"{format_value(child['value_2'])}"
                answer += '\n'
            # Или во втором
            elif type(child['value_2']) is dict:
                answer += f"{lvl * tab}- {child['key']}: " \
                          f"{format_value(child['value'])}"
                answer += '\n'
                answer += f"{lvl * tab}+ {child['key']}: "
                answer += unpack_dict(child['value_2'], lvl)
                answer += '\n'
            # Или не содержит словарей
            else:
                answer += f"{lvl * tab}- {child['key']}: " \
                      f"{format_value(child['value'])}"
                answer += '\n'
                answer += f"{lvl * tab}+ {child['key']}: " \
                          f"{format_value(child['value_2'])}"
                answer += '\n'

        # Если ключ содержит вложенные структуры
        if child['status'] == 'nested':
            answer += f"{lvl * tab}  {child['key']}: "
            answer += get_answer_str(child['value'], lvl + 2)
            answer += '\n'

        # Если ключ не поменялся и содержит словарь
        if child['status'] == 'unchanged' and type(child['value']) is dict:
            answer += f"{lvl * tab}  {child['key']}: "
            answer += unpack_dict(child['value'], lvl)
            answer += '\n'
        elif child['status'] == 'unchanged':
            answer += f"{lvl * tab}  {child['key']}: " \
                      f"{format_value(child['value'])}"
            answer += '\n'
    if lvl == 1:
        answer += '}'
    else:
        answer += f"{(lvl - 1) * tab}" + '}'
    return answer


def stylish(diff_tree):
    return get_answer_str(diff_tree)
