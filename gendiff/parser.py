import json
import yaml


def current_format(file):
    file_split = file.split('.')

    if file_split[1] == 'json':
        return 'json'
    elif file_split[1] in ['yaml', 'yml']:
        return 'yaml'



def parser(data, file_format):
    if file_format == 'json':
        return json.load(data)
    elif file_format == 'yaml':
        return yaml.load(data, Loader=yaml.FullLoader)
