import json
import yaml
import os


def get_file_extension(file_path):
    """
    Get the file extension from the file path
    :param file_path: (str) Path of the file
    :return: (str) The file extension in lowercase
    """
    _, extension = os.path.splitext(file_path)
    extension = extension.lower().lstrip('.')

    if extension == 'json':
        return 'json'

    elif extension in ['yaml', 'yml']:
        return 'yaml'


def parse_file(data, file_format):
    """
    Parse the file data based on the specified file format
    :param data: (object) Data read from the file
    :param file_format: (str) Format of the file ('json' or 'yaml')
    :return: (object) Parsed data object
    """
    if file_format == 'json':
        return json.load(data)
    elif file_format == 'yaml':
        return yaml.load(data, Loader=yaml.FullLoader)
    else:
        raise ValueError(f"Unsupported file format: {file_format}")
