import pytest
from gendiff.generate_diff import generate_diff
import sys
from gendiff.argument_parser import arg_parse


@pytest.mark.parametrize("file1,file2,extension,expected", [
    ('./tests/fixtures/test_file1.yml', './tests/fixtures/test_file2.yml', 'stylish',
     './tests/fixtures/test_answer_json.txt'),
    ('./tests/fixtures/test_file_nested1.yml', './tests/fixtures/test_file_nested2.yml', 'stylish',
     './tests/fixtures/test_tree_nested.txt'),
    ('./tests/fixtures/test_file_nested1.yml', './tests/fixtures/test_file_nested2.yml',
     'plain', './tests/fixtures/answer_flat.txt'),
    ('./tests/fixtures/test_file_nested1.yml', './tests/fixtures/test_file_nested2.yml',
     'json', './tests/fixtures/test_json.txt')])
def test_gendiff(file1, file2, extension, expected):
    assert generate_diff(file1, file2, extension) == open(expected).read()


def test_arg_parse():
    sys.argv = ['gendiff', '--format', 'plain', 'file1.json', 'file2.json']
    args = arg_parse()
    assert args.first_file == 'file1.json'
    assert args.second_file == 'file2.json'
    assert args.format == 'plain'
