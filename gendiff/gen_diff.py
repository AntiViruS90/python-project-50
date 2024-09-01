from gendiff.generator import generate_list_of_diff
from gendiff.parser import parse_file, get_file_extension
from gendiff.formatters import select_format


def read_and_parse(file):
    """
    Read and parse the contents of a file based on its extension
    :param file: (str) The path to the file
    :return: (dict) Parsed content of the file
    """
    file_format = get_file_extension(file)
    with open(file, 'r') as data:
        return parse_file(data, file_format)


def generate_diff(file_1, file_2, format_='stylish'):
    """
    Generate the difference between two files in a specified format
    :param file_1: (str) path to the first file
    :param file_2: (str) path to the second file
    :param format_: (str, optional) The format of the output diff
                    (default is 'stylish')
    :return: (str) The formatted difference between the two files
    """
    parser_data_1 = read_and_parse(file_1)
    parser_data_2 = read_and_parse(file_2)
    diff = generate_list_of_diff(parser_data_1, parser_data_2)

    output_format = select_format(format_)

    return output_format(diff)
