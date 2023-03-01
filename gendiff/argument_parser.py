#!/usr/bin/env python3

import argparse


def argument_parser():
    """display help information"""
    parser = argparse.ArgumentParser(prog='gendiff',
                                     description='Compares two '
                                                 'configuration '
                                                 'files and shows a '
                                                 'difference.')
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument('-f', '--format', default="stylish",
                        choices=['stylish', 'plain'],
                        help='set format of output')
    args = parser.parse_args()
    return args
