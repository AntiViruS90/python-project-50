def trans_value(value):
    """
    Transforms boolean True values to the string 'true',
    boolean False to the string 'false', and None values to the string 'null'.
    Other values are returned as is.

    :param value: The value to be transformed
    :return: (str) The transformed value as a string
    """
    if value is True:
        return 'true'

    elif value is False:
        return 'false'

    elif value is None:
        return 'null'

    else:
        return value
