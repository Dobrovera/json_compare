#!/usr/bin/env python3

from gendiff.argument_parser import argument_parsing
from gendiff.generate_diff import generate_diff


def main():
    arguments = argument_parsing()
    print(generate_diff(arguments.first_file, arguments.second_file,
                        arguments.format))


if __name__ == '__main__':
    main()
