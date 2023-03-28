#!/usr/bin/env python3

from gendiff.argument_parser import arg_parse
from gendiff.generate_diff import generate_diff


def main():
    arguments = arg_parse()
    print(generate_diff(arguments.first_file, arguments.second_file,
                        arguments.format))


if __name__ == '__main__':
    main()
