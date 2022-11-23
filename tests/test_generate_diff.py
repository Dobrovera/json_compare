from os import path
from gendiff.generate_diff import generate_diff, difference_tree

file1 = path.join(path.dirname("./tests/fixtures/"),
                  "test_file1.json")
file2 = path.join(path.dirname("./tests/fixtures/"),
                  "test_file2.json")
answer_str = str(path.join(path.dirname("./tests/fixtures/"),
                           "test_answer_json.txt"))
tree = str(path.join(path.dirname("./tests/fixtures/"),
                     "tree_json.txt"))


def test_gendiff_json():
    with open(answer_str) as answer:
        assert generate_diff(file1, file2) == answer.read()


def test_tree_json():
    with open(tree) as tree_dif:
        file_data = tree_dif.read()
        assert str(difference_tree(file1, file2)) == file_data
