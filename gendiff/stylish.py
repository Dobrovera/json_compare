#!/usr/bin/env python3


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
        if isinstance(child['value'], list):
            answer += f"{lvl * tab}{child['sign']} {child['key']}: "
            answer += slylish(child['value'], lvl + 2)
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
    print(diff_tree)
    return answer
