from gendiff.gen_diff import generate_diff
from gendiff.generator import generate_list_of_diff
from gendiff.parser import get_file_extension, parse_file
from gendiff.transform_func import trans_value
from gendiff.formatters.stylish import determine_type, iterate_nested_value, default_format
from gendiff.formatters.plain import plain_format, complex_or_string
from gendiff.formatters.plain import disassemble, assemble
from gendiff.formatters.json import json_format
from gendiff.formatters import select_format
import json
import yaml
import pytest

json_file_1 = "tests/fixtures/file_1.json"
json_file_2 = "tests/fixtures/file_2.json"
json_small_file = "tests/fixtures/small_file.json"
yaml_file_1 = "tests/fixtures/file_1.yaml"
yaml_file_2 = "tests/fixtures/file_2.yaml"
yaml_small_file = "tests/fixtures/small_file.yaml"
result_file = "tests/fixtures/right_result.txt"
result_file_json = "tests/fixtures/right_result_json.txt"
result_file_plain = "tests/fixtures/right_result_plain.txt"


def prepare_file(file):
    with open(file, 'r') as read_file:
        parsed_file = parse_file(read_file, get_file_extension(file))

        return parsed_file


def test_generate_diff():
    right_result = open(result_file, 'r')
    right_result = str(right_result.read())

    assert generate_diff(json_file_1, yaml_file_2) == right_result


def test_generate_list_of_diff():
    right_result = [
        {'key': 'common', 'type': 'nested', 'children': [
            {'key': 'follow', 'type': 'added', 'value': False},
            {'key': 'setting_1', 'type': 'unchanged', 'value': 'Value_1'},
            {'key': 'setting_3', 'type': 'updated', 'value_1': True, 'value_2': None}]},
        {'key': 'group_2', 'type': 'deleted', 'value': {'abc': 12345}},
        {'key': 'group_3', 'type': 'added', 'value': {"fee": 100500}}]

    data_1 = prepare_file(json_small_file)
    data_2 = prepare_file(yaml_small_file)

    assert generate_list_of_diff(data_1, data_2) == right_result


def test_default_format():
    right_result = open(result_file, 'r')

    right_result = str(right_result.read())

    json_data_1 = prepare_file(json_file_1)
    json_data_2 = prepare_file(json_file_2)

    yaml_data_1 = prepare_file(yaml_file_1)
    yaml_data_2 = prepare_file(yaml_file_2)

    assert default_format(
        generate_list_of_diff(yaml_data_1, yaml_data_2)
    ) == right_result

    assert default_format(
        generate_list_of_diff(json_data_1, json_data_2)
    ) == right_result


def test_plain():
    right_result = open(result_file_plain, 'r')

    right_result = str(right_result.read())

    json_data_1 = prepare_file(json_file_1)
    json_data_2 = prepare_file(json_file_2)

    yaml_data_1 = prepare_file(yaml_file_1)
    yaml_data_2 = prepare_file(yaml_file_2)

    assert plain_format(
        generate_list_of_diff(yaml_data_1, yaml_data_2)
    ) == right_result

    assert plain_format(
        generate_list_of_diff(json_data_1, json_data_2)
    ) == right_result


@pytest.mark.parametrize(
    'data, expected',
    [
        ({'a': '1', 'b': 2}, "[complex value]"),
        ('hello', "'hello'"),
        (25, 25)
    ]
)
def test_complex_or_string(data, expected):
    assert complex_or_string(data) == expected


def test_disassemble():
    example_value = [
        {'key': 'common', 'type': 'nested', 'children': [
            {'key': 'follow', 'type': 'added', 'value': False},
            {'key': 'setting_1', 'type': 'unchanged', 'value': 'Value_1'}]}]

    right_result = ['common.follow', 'added', 'false']

    assert disassemble(example_value) == right_result


def test_assemble():
    assert assemble([1, 2, 3, 4, 5, 6]) == [[1, 2, 3], [4, 5, 6]]


def test_json_format():
    right_result = open(result_file_json, 'r')

    right_result = str(right_result.read())

    json_data_1 = prepare_file(json_file_1)
    json_data_2 = prepare_file(json_file_2)

    yaml_data_1 = prepare_file(yaml_file_1)
    yaml_data_2 = prepare_file(yaml_file_2)

    assert json_format(
        generate_list_of_diff(yaml_data_1, yaml_data_2)
    ) == right_result

    assert json_format(
        generate_list_of_diff(json_data_1, json_data_2)
    ) == right_result


@pytest.mark.parametrize(
    'stile_format, expected_format',
    [
        ('stylish', default_format),
        ('plain', plain_format),
        ('json', json_format)
    ]
)
def test_select_format(stile_format, expected_format):
    assert select_format(stile_format) == expected_format


@pytest.mark.parametrize(
    'value, expected_value',
    [
        (True, 'true'),
        (False, 'false'),
        (None, 'null'),
        ('120.120', '120.120'),
    ]
)
def test_trans_value(value, expected_value):
    assert trans_value(value) == expected_value


@pytest.mark.parametrize(
    'determine, expected_type',
    [
        ('added', '+ '),
        ('deleted', '- '),
        ('changed', '  '),
    ]
)
def test_trans_type(determine, expected_type):
    assert determine_type(determine) == expected_type


def test_iterate_nested_value():
    nested_value = {'2': {'3': '#'}, 'x': 1}
    right_result = '{\n  2: {\n      3: #\n  }\n  x: 1\n}'
    assert iterate_nested_value(nested_value, 2) == right_result


@pytest.mark.parametrize(
    'file_path, expected_extension',
    [
        ("tests/fixtures/file_1.json", 'json'),
        ("tests/fixtures/file_1.yaml", 'yaml'),
    ]
)
def test_get_file_extension(file_path, expected_extension):
    assert get_file_extension(file_path) == expected_extension


right_result_1 = open(json_file_1)
right_result_2 = open(yaml_file_1)


def test_parser():
    with open(json_file_1, 'r') as json_file:
        assert parse_file(json_file, 'json') == json.load(right_result_1)

    with open(yaml_file_1, 'r') as yaml_file:
        assert (parse_file(yaml_file, 'yaml') == yaml.load(
            right_result_2, Loader=yaml.FullLoader
        ))
