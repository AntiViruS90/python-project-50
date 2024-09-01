import json


def json_format(list_of_diff):
    return json.dumps(list_of_diff[0], indent=2)
