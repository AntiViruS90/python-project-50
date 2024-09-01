#!/usr/bin/env python3

from gendiff.cli import argparse_func
from gendiff.gen_diff import generate_diff


def main():
    args = argparse_func()
    diff = generate_diff(args.first_file, args.second_file, args.format)

    print(diff)


if __name__ == '__main__':
    main()
