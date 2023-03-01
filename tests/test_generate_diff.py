from os import path
from gendiff.generate_diff import generate_diff, difference_tree
import sys
from gendiff.argument_parser import argument_parser

file1 = path.join(path.dirname("./tests/fixtures/"),
                  "test_file1.json")
file2 = path.join(path.dirname("./tests/fixtures/"),
                  "test_file2.json")
file1_yml = path.join(path.dirname("./tests/fixtures/"),
                      "test_file1.yml")
file2_yml = path.join(path.dirname("./tests/fixtures/"),
                      "test_file2.yml")
answer_str = str(path.join(path.dirname("./tests/fixtures/"),
                           "test_answer_json.txt"))
answer_flat = str(path.join(path.dirname("./tests/fixtures/"),
                           "answer_flat.txt"))
tree = str(path.join(path.dirname("./tests/fixtures/"),
                     "tree_json.txt"))
nested_yml_1 = path.join(path.dirname("./tests/fixtures/"),
                         "test_file_nested1.yml")
nested_yml_2 = path.join(path.dirname("./tests/fixtures/"),
                         "test_file_nested2.yml")
nested_tree = str(path.join(path.dirname("./tests/fixtures/"),
                            "tree_nested.txt"))


def test_gendiff_json():
    with open(answer_str) as answer:
        assert generate_diff(file1, file2) == answer.read()


def test_tree_json():
    with open(tree) as tree_dif:
        file_data = tree_dif.read()
        assert str(difference_tree(file1, file2)) == file_data


def test_gendiff_yml():
    with open(answer_str) as answer:
        assert generate_diff(file1_yml, file2_yml, format_name='stylish') == answer.read()


def test_nested():
    with open(nested_tree) as tr:
        file_data = tr.read()
        assert str(difference_tree(nested_yml_1, nested_yml_2)) == file_data


def test_flat():
    with open(answer_flat) as an:
        assert generate_diff(nested_yml_1, nested_yml_2, format_name='plain') == an.read()



def test_arg_parse():
    sys.argv = ['gendiff', '--format', 'plain', 'file1.json', 'file2.json']
    args = argument_parser()
    assert args.first_file == 'file1.json'
    assert args.second_file == 'file2.json'
    assert args.format == 'plain'