from gendiff.formats.plain import plain_format
from gendiff.formats.stylish import default_format
from gendiff.formats.json import json_format


def select_format(output_format):

    if output_format == 'stylish':
        return default_format

    elif output_format == 'plain':
        return plain_format

    elif output_format == 'json':
        return json_format
