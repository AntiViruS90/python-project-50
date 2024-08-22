from gendiff.generator import generate_list_of_diff
from gendiff.parser import parser, current_format
from gendiff.formats.select_format import select_format


def generate_diff(file_1, file_2, format_='stylish'):
    with open(file_1, 'r') as data_1, open(file_2, 'r') as data_2:
        parser_data_1 = parser(data_1, current_format(file_1))
        parser_data_2 = parser(data_2, current_format(file_2))
        output_format = select_format(format_)
        diff = generate_list_of_diff(parser_data_1, parser_data_2)

        return output_format(diff)
