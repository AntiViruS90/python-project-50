import itertools
from gendiff.transform_func import trans_value


def complex_or_string(value):
    if isinstance(value, dict):
        return '[complex value]'
    elif isinstance(value, str):
        return f"{value}"
    else:
        return value


def disassemble(list_of_diff):
    def iter_(keys, path=''):
        lines = []

        for key in keys:
            name = f"{key['key']}"

            if key['type'] == 'added':
                lines.append(
                    [path + name,
                     'added',
                     trans_value(complex_or_string(key['value']))]
                )
            elif key['type'] == 'deleted':
                lines.append(
                    [path + name,
                     'removed',
                     trans_value(complex_or_string(key['value']))]
                )
            elif key['type'] == 'updated':
                lines.append(
                    [
                        path + name, 'updated',
                        [trans_value(complex_or_string(key['value_1'])),
                        trans_value(complex_or_string(key['value_2']))]
                    ]
                )
            elif key['type'] == 'nested':
                lines.append(iter_(key['children'], path + name + '.'))

        result = itertools.chain(lines)

        return sum(list(result), [])

    return iter_(list_of_diff)


def assemble(list_of_keys, n=3):
    result = [list_of_keys[i:i + n] for i in range(0, len(list_of_keys), n)]

    return result


def plain_format(list_of_diff):
    disassembled_keys = disassemble(list_of_diff)
    assembled_keys = assemble(disassembled_keys)

    result = ''

    for key in assembled_keys:

        if key[1] == 'added':
            result += f"Property: '{key[0]}' "
            result += f"was added with value: {key[2]}\n"

        elif key[1] == 'removed':
            result += f"Property: '{key[0]}' was removed\n"

        else:
            result += f"Property: '{key[0]}' "
            result += f"was updated. From '{key[2][0]}' to '{key[2][1]}'\n"

    return result[:-1]
