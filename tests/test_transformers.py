import xmltodict3.transformers as transformers


def test_integer_transformation_1():
    element = transformers.IntegerTransformer()
    node_data = {'@type': 'integer', '#text': '1'}
    expected_result = {'#text': 1}
    result = element.transform_node(node_data)
    assert result == expected_result, result


def test_integer_transformation_2():
    element = transformers.IntegerTransformer()
    node_data = {'@type': 'integer', '#text': '1', '@attr': 'attr'}
    expected_result = {'#text': 1, '@attr': 'attr'}
    result = element.transform_node(node_data)
    assert result == expected_result, result


def test_integer_transformation_wrong_type():
    element = transformers.IntegerTransformer()
    node_data = {'@type': 'float', '#text': '1', '@attr': 'attr'}
    expected_result = {'@type': 'float', '#text': '1', '@attr': 'attr'}
    result = element.transform_node(node_data)
    assert result == expected_result, result


def test_bool_transformation_true_1():
    element = transformers.BoolTransformer()
    node_data = {'@type': 'bool', '#text': 'true'}
    expected_result = {'#text': True}
    result = element.transform_node(node_data)
    assert result == expected_result, result


def test_bool_transformation_true_2():
    element = transformers.BoolTransformer()
    node_data = {'@type': 'bool', '#text': 'True'}
    expected_result = {'#text': True}
    result = element.transform_node(node_data)
    assert result == expected_result, result


def test_bool_transformation_false_1():
    element = transformers.BoolTransformer()
    node_data = {'@type': 'bool', '#text': 'false'}
    expected_result = {'#text': False}
    result = element.transform_node(node_data)
    assert result == expected_result, result


def test_bool_transformation_false_2():
    element = transformers.BoolTransformer()
    node_data = {'@type': 'bool', '#text': 'true1'}
    expected_result = {'#text': False}
    result = element.transform_node(node_data)
    assert result == expected_result, result
