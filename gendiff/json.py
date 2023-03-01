#!/usr/bin/env python3


import json


def f_json(diff_tree):
    return json.dumps(diff_tree, indent=4, sort_keys=True)
