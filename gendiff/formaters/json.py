import json


def f_json(diff_tree):
    return json.dumps(diff_tree, indent=4)