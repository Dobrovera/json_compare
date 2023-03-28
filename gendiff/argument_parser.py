import argparse


def arg_parse():
    """display help information"""
    parser = argparse.ArgumentParser(prog='gendiff',
                                     description='Compares two '
                                                 'configuration '
                                                 'files and shows a '
                                                 'difference.')
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument('-f', '--format', default="stylish",
                        choices=['stylish', 'plain', 'json'],
                        help='set format of output')
    args = parser.parse_args()
    return args
