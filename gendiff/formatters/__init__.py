from gendiff.formatters.plain import plain_format
from gendiff.formatters.stylish import default_format
from gendiff.formatters.json import json_format


def select_format(output_format):
    """
    Selects and returns a specific formatting function based
    on the given output format
    :param output_format: (str) The output format to select. Valid values
                        are 'stulish', 'plain', or 'json'
    :return: (func) The formatting function corresponding to the output format
    """

    if output_format == 'stylish':
        return default_format

    elif output_format == 'plain':
        return plain_format

    elif output_format == 'json':
        return json_format
