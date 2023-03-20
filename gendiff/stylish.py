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


def slylish(diff_tree: object, lvl: object = 1) -> object:
    tab = "  "
    answer = '{\n'
    for child in diff_tree:
        if child['value'] is True:
            child['value'] = 'true'
        elif child['value'] is False:
            child['value'] = 'false'
        elif child['value'] is None:
            child['value'] = 'null'
        # Если ключ был удален
        if child['status'] == 'removed':
            # И содержит словарь
            if type(child['value']) is dict:
                answer += f"{lvl * tab}- {child['key']}: "
                r = unpack_dict(child['value'], lvl * tab, lvl)
                answer += r
                answer += '\n'
            else:
                answer += f"{lvl * tab}- {child['key']}: " \
                      f"{child['value']}"
                answer += '\n'
        # Если ключ был добавлен во второй файл
        elif child['status'] == 'added':
            # И содержит словарь
            if type(child['value']) is dict:
                answer += f"{lvl * tab}+ {child['key']}: "
                r = unpack_dict(child['value'], lvl * tab, lvl)
                answer += r
                answer += '\n'
            else:
                answer += f"{lvl * tab}+ {child['key']}: " \
                      f"{child['value']}"
                answer += '\n'
        # Если ключ поменялся
        elif child['status'] == 'changed':
            if child['value_2'] is True:
                child['value_2'] = 'true'
            elif child['value_2'] is False:
                child['value_2'] = 'false'
            elif child['value_2'] is None:
                child['value_2'] = 'null'
            # И содержит словарь в первом файле
            if type(child['value']) is dict:
                answer += f"{lvl * tab}+ {child['key']}: "
                r = unpack_dict(child['value'], lvl * tab, lvl)
                answer += r
                answer += '\n'
            # Или во втором
            elif type(child['value_2']) is dict:
                answer += f"{lvl * tab}+ {child['key']}: "
                r = unpack_dict(child['value_2'], lvl * tab, lvl)
                answer += r
                answer += '\n'
            else:
                answer += f"{lvl * tab}- {child['key']}: " \
                      f"{child['value']}"
                answer += '\n'
                answer += f"{lvl * tab}+ {child['key']}: " \
                          f"{child['value_2']}"
                answer += '\n'
        # Если ключ сожержит вложенные структуры
        elif child['status'] == 'nested':
            answer += f"{lvl * tab}  {child['key']}: "
            answer += slylish(child['value'], lvl + 2)
            answer += '\n'
        # Если ключ не поменялся
        elif child['status'] == 'unchanged':
            # И содержит словарь
            if type(child['value']) is dict:
                answer += f"{lvl * tab}  {child['key']}: "
                r = unpack_dict(child['value'], lvl * tab, lvl)
                answer += r
                answer += '\n'
            else:
                answer += f"{lvl * tab}  {child['key']}: " \
                         f"{child['value']}"
                answer += '\n'
    if lvl == 1:
        answer += '}'
    else:
        answer += f"{(lvl - 1) * tab}" + '}'
    return answer
