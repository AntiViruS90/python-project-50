from gendiff.gen_diff import generate_diff
from gendiff.generator import generate_list_of_diff
from gendiff.parser import current_format, parser
from gendiff.transform_func import trans_type, trans_nested_value, trans_value
from gendiff.formats.stylish import default_format
from gendiff.formats.plain import plain_format, complex_or_string
from gendiff.formats.plain import disassemble, assemble
from gendiff.formats.json import json_format
from gendiff.formats.select_format import select_format
import json
import yaml

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
        parsed_file = parser(read_file, current_format(file))

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


def test_complex_or_string():
    assert complex_or_string({'a': '1', 'b': 2}) == "[complex value]"
    assert complex_or_string('hello') == "hello"
    assert complex_or_string(25) == 25


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


def test_select_format():
    assert select_format('stylish') == default_format
    assert select_format('plain') == plain_format
    assert select_format('json') == json_format


def test_trans_value():
    assert trans_value(True) == 'true'
    assert trans_value(False) == 'false'
    assert trans_value(None) == 'null'
    assert trans_value('120.120') == '120.120'


def test_trans_type():
    assert trans_type('added') == '+ '
    assert trans_type('deleted') == '- '
    assert trans_type('changed') == '  '


def test_trans_nested_value():
    nested_value = {'2': {'3': '#'}, 'x': 1}
    right_result = '{\n  2: {\n      3: #\n  }\n  x: 1\n}'
    assert trans_nested_value(nested_value, 2) == right_result


def test_current_format():
    assert current_format("tests/fixtures/file_1.json") == 'json'
    assert current_format("tests/fixtures/file_1.yaml") == 'yaml'


right_result_1 = open(json_file_1)
right_result_2 = open(yaml_file_1)


def test_parser():
    with open(json_file_1, 'r') as json_file:
        assert parser(json_file, 'json') == json.load(right_result_1)

    with open(yaml_file_1, 'r') as yaml_file:
        assert (parser(yaml_file, 'yaml') == yaml.load(
            right_result_2, Loader=yaml.FullLoader
        ))
