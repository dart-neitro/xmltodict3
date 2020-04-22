import datetime

import pytest

import xmltodict3.transformers as transformers


def test_integer_transformation_1():
    transformer = transformers.IntegerTransformer()
    node_data = {'@type': 'integer', '#text': '1'}
    expected_result = {'@type': 'integer', '#text': 1}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_integer_transformation_with_type_removing():
    transformer = transformers.IntegerTransformer(removing_types=True)
    node_data = {'@type': 'integer', '#text': '1'}
    expected_result = {'#text': 1}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_integer_transformation_invalid_execute():
    transformer = transformers.IntegerTransformer()
    node_data = {'#text': '1'}
    expected_result = {'#text': '1'}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_integer_transformation_2():
    transformer = transformers.IntegerTransformer(removing_types=True)
    node_data = {'@type': 'integer', '#text': '1', '@attr': 'attr'}
    expected_result = {'#text': 1, '@attr': 'attr'}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_integer_transformation_invalid_type():
    transformer = transformers.IntegerTransformer(removing_types=True)
    node_data = {'@type': 'float', '#text': '1', '@attr': 'attr'}
    expected_result = {'@type': 'float', '#text': '1', '@attr': 'attr'}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_integer_transformation_none():
    transformer = transformers.IntegerTransformer()
    node_data = {'@type': 'integer', '#text': None}
    with pytest.raises(transformers.TransformerException):
        transformer.transform_node(node_data)


def test_integer_transformation_none_with_ignore_errors():
    transformer = transformers.IntegerTransformer(ignore_errors=True)
    node_data = {'@type': 'integer', '#text': None}
    expected_result = {'@type': 'integer', '#text': None}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_integer_transformation_with_exception():
    transformer = transformers.IntegerTransformer(ignore_errors=False)
    node_data = {'@type': 'integer', '#text': None}
    with pytest.raises(transformers.TransformerException):
        transformer.transform_node(node_data)

    node_data = {'@type': 'integer', '#text': 'None'}
    with pytest.raises(transformers.TransformerException):
        transformer.transform_node(node_data)


def test_integer_transformation_without_text():
    transformer = transformers.IntegerTransformer(removing_types=True)
    node_data = {'@type': 'integer'}
    expected_result = {'@type': 'integer'}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_bool_transformation_true_1():
    transformer = transformers.BoolTransformer(removing_types=True)
    node_data = {'@type': 'bool', '#text': 'true'}
    expected_result = {'#text': True}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_bool_transformation_true_2():
    transformer = transformers.BoolTransformer(removing_types=True)
    node_data = {'@type': 'bool', '#text': 'True'}
    expected_result = {'#text': True}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_bool_transformation_false_1():
    transformer = transformers.BoolTransformer(removing_types=True)
    node_data = {'@type': 'bool', '#text': 'false'}
    expected_result = {'#text': False}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_bool_transformation_false_2():
    transformer = transformers.BoolTransformer(
        removing_types=True, ignore_errors=True)
    node_data = {'@type': 'bool', '#text': 'true1'}
    expected_result = {'#text': 'true1'}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_bool_transformation_false_none():
    transformer = transformers.BoolTransformer(
        removing_types=True, ignore_errors=True)
    node_data = {'@type': 'bool', '#text': None}
    expected_result = {'#text': None}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_datetime_transformation():
    transformer = transformers.DateTimeTransformer(removing_types=True)
    node_data = {'@type': 'datetime', '#text': '2020-02-12T20:20:46Z'}
    expected_result = {'#text': datetime.datetime(2020, 2, 12, 20, 20, 46)}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_datetime_transformation_none():
    transformer = transformers.DateTimeTransformer(
        removing_types=True, ignore_errors=True)
    node_data = {'@type': 'datetime', '#text': '2020-02-12 20:20:46'}
    expected_result = {'#text': '2020-02-12 20:20:46'}
    result = transformer.transform_node(node_data)
    assert result == expected_result, result


def test_datetime_transformation_custom_datetime_format():
    transformer = transformers.DateTimeTransformer(removing_types=True)
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
    pull_transformers.set_removing_types(True)

    node_data = {'@type': 'datetime', '#text': '2020-02-12T20:20:46Z'}
    expected_result = {'#text': datetime.datetime(2020, 2, 12, 20, 20, 46)}
    result = pull_transformers.transform_node(node_data)

    assert result == expected_result, result


def test_pull_transformers_invalid_value():
    transformer_list = transformers.DefaultTransformerList
    pull_transformers = transformers.PullTransformers(*transformer_list)

    node_data = {'@type': 'datetime', '#text': '2020-02-12 20:20:46Z'}
    with pytest.raises(transformers.TransformerException):
        pull_transformers.transform_node(node_data)


def test_pull_transformers_exception():
    transformer_list = transformers.DefaultTransformerList
    pull_transformers = transformers.PullTransformers(*transformer_list)
    pull_transformers.set_ignore_errors(False)

    node_data = {'@type': 'datetime', '#text': '2020-02-12 20:20:46Z'}

    with pytest.raises(transformers.TransformerException):
        pull_transformers.transform_node(node_data)


class PriceTransformer(transformers.AbstractTransformer):
    key = "price"

    def get_value_or_raise_exception(self, node_data):
        return int(node_data['#text'])


def test_pull_transformers_class():
    transformer_list = [PriceTransformer]
    pull_transformers = transformers.PullTransformers(*transformer_list)

    node_data = {'@type': 'price', '#text': '220'}
    expected_result = {'@type': 'price', '#text': 220}
    result = pull_transformers.transform_node(node_data)

    assert result == expected_result, result


def test_pull_transformers_instance():
    transformer_list = [PriceTransformer()]
    pull_transformers = transformers.PullTransformers(*transformer_list)

    node_data = {'@type': 'price', '#text': '111'}
    expected_result = {'@type': 'price', '#text': 111}
    result = pull_transformers.transform_node(node_data)

    assert result == expected_result, result
