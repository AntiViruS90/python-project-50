def generate_list_of_diff(data_1, data_2):
    def run(curr_data_1, curr_data_2):
        result = []

        for key in sorted(curr_data_1.keys() | curr_data_2.keys()):
            if (key in curr_data_1) and (key in curr_data_2) \
                    and curr_data_1[key] == curr_data_2[key]:
                result.append({
                    'key': key,
                    'type': 'unchanged',
                    'value': curr_data_1[key]
                })
            elif key not in curr_data_1:
                result.append({
                    'key': key,
                    'type': 'added',
                    'value': curr_data_2[key]
                })
            elif key not in curr_data_2:
                result.append({
                    'key': key,
                    'type': 'deleted',
                    'value': curr_data_1[key]
                })
            elif isinstance(curr_data_1[key], dict) \
                    and isinstance(curr_data_2[key], dict):
                result.append({
                    'key': key,
                    'type': 'nested',
                    'children': run(curr_data_1[key], curr_data_2[key])
                })
            else:
                result.append({
                    'key': key,
                    'type': 'updated',
                    'value_1': curr_data_1[key],
                    'value_2': curr_data_2[key]
                })
        return result
    return run(data_1, data_2)
