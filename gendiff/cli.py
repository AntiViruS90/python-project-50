import argparse


def argparse_func():
    """
    Parses command line arguments for the gendiff utility
    :return: argparse.Namespace: An object that stores the command-line arguments
            parsed by argparse
    """
    parser = argparse.ArgumentParser(
        usage="gendiff [-h] [-f FORMAT] first_file second_file",
        description="Compares two configuration files and shows a difference"
    )

    parser.add_argument("first_file")
    parser.add_argument("second_file")
    parser.add_argument(
        '-f', '--format',
        default="stylish",
        help="set format of output"
    )

    args = parser.parse_args()

    return args
