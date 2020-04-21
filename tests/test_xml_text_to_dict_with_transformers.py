import datetime

from xmltodict3 import XmlTextToDict
import xmltodict3.transformers as transformers


def test_xml_text_to_dict_with_default_transformers_simple_case():
    text = """

    <int_value type="integer">
        222
    </int_value>

    """
    expected_result = {'int_value': 222}

    transformer_list = transformers.DefaultTransformerList
    pull_transformers = transformers.PullTransformers(*transformer_list)

    xml_to_dict = XmlTextToDict(text)
    xml_to_dict.use_pull_transformers(pull_transformers)

    result = xml_to_dict.get_dict()

    assert result == expected_result, result


def test_xml_text_to_dict_with_default_transformers():
    text = """
    <root>
        <values>
            <int_value type="integer">
                123
            </int_value>
        </values>
    </root>
    """
    expected_result = {'root': {'values': {'int_value': 123}}}

    transformer_list = transformers.DefaultTransformerList
    pull_transformers = transformers.PullTransformers(*transformer_list)

    xml_to_dict = XmlTextToDict(text)
    xml_to_dict.use_pull_transformers(pull_transformers)

    result = xml_to_dict.get_dict()

    assert result == expected_result, result


def test_xml_text_to_dict_with_default_transformers_2():
    text = """
    <root>
        <values>
            <int_value type="integer">
                42
            </int_value>
            <bool_value type="bool">
                true
            </bool_value>
            <bool_value2 type="bool">
                false
            </bool_value2>
            <clear_value>
                clear_value
            </clear_value>
            <timestamp type="datetime">
                2021-02-12T20:20:46Z
            </timestamp>
            <tag_with_not_implemented_type type="not_implemented_type">
                value
            </tag_with_not_implemented_type>
            <empty_tag type="not_implemented_type" />
        </values>
    </root>
    """
    expected_result = {'root': {'values': {
        'int_value': 42, 'bool_value': True,
        'bool_value2': False, 'clear_value': 'clear_value',
        'timestamp': datetime.datetime(2021, 2, 12, 20, 20, 46),
        'tag_with_not_implemented_type': {
            '#text': 'value', '@type': 'not_implemented_type'},
        'empty_tag': {
            '#text': None, '@type': 'not_implemented_type'},
    }}}

    transformer_list = transformers.DefaultTransformerList
    pull_transformers = transformers.PullTransformers(*transformer_list)

    xml_to_dict = XmlTextToDict(text)
    xml_to_dict.use_pull_transformers(pull_transformers)

    result = xml_to_dict.get_dict()

    assert result == expected_result, result
