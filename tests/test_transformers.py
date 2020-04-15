import datetime

import pytest

import xmltodict3.transformers as transformers


def test_integer_transformation_1():
    transformer = transformers.IntegerTransformer()
    node_data = {'@type': 'integer', '#text': '1'}
    expected_result = {'#text': 1}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_integer_transformation_2():
    transformer = transformers.IntegerTransformer()
    node_data = {'@type': 'integer', '#text': '1', '@attr': 'attr'}
    expected_result = {'#text': 1, '@attr': 'attr'}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_integer_transformation_wrong_type():
    transformer = transformers.IntegerTransformer()
    node_data = {'@type': 'float', '#text': '1', '@attr': 'attr'}
    expected_result = {'@type': 'float', '#text': '1', '@attr': 'attr'}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_integer_transformation_none():
    transformer = transformers.IntegerTransformer()
    node_data = {'@type': 'integer', '#text': None}
    expected_result = {'#text': None}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_integer_transformation_with_exception():
    transformer = transformers.IntegerTransformer(using_default_value=False)
    node_data = {'@type': 'integer', '#text': None}
    with pytest.raises(transformers.TransformerException):
        transformer.transform_node(node_data)

    node_data = {'@type': 'integer', '#text': 'None'}
    with pytest.raises(transformers.TransformerException):
        transformer.transform_node(node_data)


def test_integer_transformation_without_text():
    transformer = transformers.IntegerTransformer()
    node_data = {'@type': 'integer'}
    expected_result = {'@type': 'integer'}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_bool_transformation_true_1():
    transformer = transformers.BoolTransformer()
    node_data = {'@type': 'bool', '#text': 'true'}
    expected_result = {'#text': True}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_bool_transformation_true_2():
    transformer = transformers.BoolTransformer()
    node_data = {'@type': 'bool', '#text': 'True'}
    expected_result = {'#text': True}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_bool_transformation_false_1():
    transformer = transformers.BoolTransformer()
    node_data = {'@type': 'bool', '#text': 'false'}
    expected_result = {'#text': False}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_bool_transformation_false_2():
    transformer = transformers.BoolTransformer()
    node_data = {'@type': 'bool', '#text': 'true1'}
    expected_result = {'#text': None}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_bool_transformation_false_none():
    transformer = transformers.BoolTransformer()
    node_data = {'@type': 'bool', '#text': None}
    expected_result = {'#text': None}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_datetime_transformation():
    transformer = transformers.DateTimeTransformer()
    node_data = {'@type': 'datetime', '#text': '2020-02-12T20:20:46Z'}
    expected_result = {'#text': datetime.datetime(2020, 2, 12, 20, 20, 46)}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_datetime_transformation_none():
    transformer = transformers.DateTimeTransformer()
    node_data = {'@type': 'datetime', '#text': '2020-02-12 20:20:46'}
    expected_result = {'#text': None}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_datetime_transformation_custom_datetime_format():
    transformer = transformers.DateTimeTransformer()
    transformer.set_datetime_format("%Y-%m-%d %H:%M:%S")
    node_data = {'@type': 'datetime', '#text': '2020-02-12 20:20:46'}
    expected_result = {'#text': datetime.datetime(2020, 2, 12, 20, 20, 46)}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_pull_transformers_no_transformer():
    transformer_list = transformers.DefaultTransformerList
    pull_transformers = transformers.PullTransformers(*transformer_list)

    node_data = {'@type': 'fake_type', '#text': 'bla-bla-bla'}
    expected_result = node_data
    result = pull_transformers.transform_node(node_data)

    assert result == expected_result, result


def test_pull_transformers():
    transformer_list = transformers.DefaultTransformerList
    pull_transformers = transformers.PullTransformers(*transformer_list)

    node_data = {'@type': 'datetime', '#text': '2020-02-12T20:20:46Z'}
    expected_result = {'#text': datetime.datetime(2020, 2, 12, 20, 20, 46)}
    result = pull_transformers.transform_node(node_data)

    assert result == expected_result, result


def test_pull_transformers_wrong_value():
    transformer_list = transformers.DefaultTransformerList
    pull_transformers = transformers.PullTransformers(*transformer_list)

    node_data = {'@type': 'datetime', '#text': '2020-02-12 20:20:46Z'}
    expected_result = {'#text': None}
    result = pull_transformers.transform_node(node_data)

    assert result == expected_result, result


def test_pull_transformers_exception():
    transformer_list = transformers.DefaultTransformerList
    pull_transformers = transformers.PullTransformers(*transformer_list)
    pull_transformers.set_using_default_value(False)

    node_data = {'@type': 'datetime', '#text': '2020-02-12 20:20:46Z'}

    with pytest.raises(transformers.TransformerException):
        pull_transformers.transform_node(node_data)
