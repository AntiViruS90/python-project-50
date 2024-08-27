import json
import yaml


def current_format(file):
    if file[-4:] == 'json':
        return 'json'

    elif file[-4:] in ['yaml', '.yml']:
        return 'yaml'


def parser(data, file_format):
    if file_format == 'json':
        return json.load(data)
    elif file_format == 'yaml':
        return yaml.load(data, Loader=yaml.FullLoader)
