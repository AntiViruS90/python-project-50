import itertools

from gendiff.transform_func import trans_value


def iterate_nested_value(value, spaces_count, replacer=' '):
    """
    Recursively iterates over a nested dictionary and formats it into in string
    with specified indentation

    Args:
    :param value: (dict) The nested dictionary to iterate over
    :param spaces_count: (int) The initial number of spaces for indentation
    :param replacer: (str, optional) The character used for indentation.
                    Defaults to ' '

    :return: (str) The formatted string representation of the nested dictionary
            with appropriate indentation
    """
    if not isinstance(value, dict):
        return trans_value(value)

    def iter_(nested_value, spaces_count_1):
        lines = []

        for key, value in nested_value.items():
            if not isinstance(value, dict):
                lines.append(
                    f"{replacer * spaces_count_1}{key}: "
                    f"{trans_value(value)}"
                )
            else:
                lines.append(
                    f"{replacer * spaces_count_1}{key}: "
                    f"{iter_(value, spaces_count_1 + 4)}"
                )
        result = itertools.chain(
            "{", lines, [(replacer * (spaces_count_1 - 4)) + "}"]
        )

        return '\n'.join(result)

    return iter_(value, spaces_count)


def determine_type(type_of_key):
    """
    Determine the representation character based on the type of key
    :param type_of_key: (str) The type of key ('added', 'deleted' or any other)
    :return: (str) The representation character ('+ ', '- ', or '  ')
    """
    if type_of_key == 'added':
        return '+ '
    elif type_of_key == 'deleted':
        return '- '
    else:
        return '  '


def default_format(list_of_diff, replacer=' '):
    """
    Generate the default format representation of the list of differences
    :param list_of_diff: (list) A list of difference objects.
    :param replacer: (str, optional) The character used for indentation.
                    Defaults to ' '
    :return: (str) The formatted representation of the differences
    """
    def iter_(current_value, spaces_count):
        lines = []

        for key in current_value:
            if key['type'] == 'nested':
                lines.append(
                    f"{replacer * spaces_count}  "
                    f"{key['key']}: "
                    f"{iter_(key['children'], spaces_count + 4)}"
                )
            elif key['type'] == 'updated':
                lines.append(
                    f"{replacer * spaces_count}- "
                    f"{key['key']}: "
                    f"{iterate_nested_value(key['value_1'], spaces_count + 6)}"
                )
                lines.append(
                    f"{replacer * spaces_count}+ "
                    f"{key['key']}: "
                    f"{iterate_nested_value(key['value_2'], spaces_count + 6)}"
                )
            else:
                lines.append(
                    f"{replacer * spaces_count}{determine_type(key['type'])}"
                    f"{key['key']}: "
                    f"{iterate_nested_value(key['value'], spaces_count + 6)}"
                )
        result = itertools.chain(
            "{", lines, [(replacer * (spaces_count - 2)) + "}"]
        )

        return '\n'.join(result)

    return iter_(list_of_diff, 2)
