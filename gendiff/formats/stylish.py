import itertools
from gendiff.transform_func import trans_type, trans_nested_value


def default_format(list_of_diff, replacer=' '):
    def iter_(current_value, spaces_count):
        lines = []

        for key in current_value:
            if key['type'] == 'nested':
                lines.append(
                    f"{replacer * spaces_count} "
                    f"{key['key']}: "
                    f"{iter_(key['children'], spaces_count + 4)}"
                )
            elif key['type'] == 'updated':
                lines.append(
                    f"{replacer * spaces_count}- "
                    f"{key['key']}: "
                    f"{trans_nested_value(key['value_1'], spaces_count + 6)}"
                )
                lines.append(
                    f"{replacer * spaces_count}+ "
                    f"{key['key']}: "
                    f"{trans_nested_value(key['value_2'], spaces_count + 6)}"
                )
            else:
                lines.append(
                    f"{replacer * spaces_count}{trans_type(key['type'])}"
                    f"{key['key']}: "
                    f"{trans_nested_value(key['value'], spaces_count + 6)}"
                )
        result = itertools.chain(
            "{", lines, [(replacer * (spaces_count - 2)) + "}"]
        )

        return '\n'.join(result)

    return iter_(list_of_diff, 2)
