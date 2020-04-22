import datetime
import xml.etree.ElementTree as ElementTree

from xmltodict3 import XmlToDict
import xmltodict3.transformers as transformers


def test_xml_to_dict_with_default_transformers_simple_case():
    text = """

    <int_value type="integer">
        111
    </int_value>

    """
    expected_result = {'int_value': {'#text': 111, '@type': "integer"}}

    transformer_list = transformers.DefaultTransformerList
    pull_transformers = transformers.PullTransformers(*transformer_list)

    etree_element = ElementTree.fromstring(text)
    xml_to_dict = XmlToDict(etree_element)
    xml_to_dict.use_pull_transformers(pull_transformers)

    result = xml_to_dict.get_dict()

    assert result == expected_result, result


def test_xml_to_dict_with_default_transformers():
    text = """
    <root>
        <values>
            <int_value type="integer">
                111
            </int_value>
        </values>
    </root>
    """
    expected_result = {'root': {'values': {'int_value': 111}}}

    transformer_list = transformers.DefaultTransformerList
    pull_transformers = transformers.PullTransformers(*transformer_list)
    pull_transformers.set_removing_types(True)

    etree_element = ElementTree.fromstring(text)
    xml_to_dict = XmlToDict(etree_element)
    xml_to_dict.use_pull_transformers(pull_transformers)

    result = xml_to_dict.get_dict()

    assert result == expected_result, result


def test_xml_to_dict_with_default_transformers_2():
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
                2020-02-12T20:20:46Z
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
        'timestamp': datetime.datetime(2020, 2, 12, 20, 20, 46),
        'tag_with_not_implemented_type': {
            '#text': 'value', '@type': 'not_implemented_type'},
        'empty_tag': {
            '#text': None, '@type': 'not_implemented_type'},
    }}}

    transformer_list = transformers.DefaultTransformerList
    pull_transformers = transformers.PullTransformers(*transformer_list)
    pull_transformers.set_removing_types(True)

    etree_element = ElementTree.fromstring(text)
    xml_to_dict = XmlToDict(etree_element)
    xml_to_dict.use_pull_transformers(pull_transformers)

    result = xml_to_dict.get_dict()

    assert result == expected_result, result
