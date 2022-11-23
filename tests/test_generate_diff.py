from os import path
from gendiff.generate_diff import difference_tree, generate_diff


def test_gendiff_json():
    file1 = path.join(path.dirname("./fixtures/"),
                      "test_file1.json")
    file2 = path.join(path.dirname("./fixtures/"),
                      "test_file2.json")
    answer_str = str(path.join(path.dirname("./fixtures/"),
                               "test_answer_json.txt"))
    with open(answer_str) as answer:
        assert generate_diff(file1, file2) == answer.read()

