#!/usr/bin/env python3

from gendiff.cli import args
from gendiff.gen_diff import generate_diff


def main():
    diff = generate_diff(args.first_file, args.second_file, args.format)

    print(diff)


if __name__ == '__main__':
    main()
