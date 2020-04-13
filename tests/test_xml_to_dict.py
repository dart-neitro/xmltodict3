import xml.etree.ElementTree as ElementTree

from xmltodict3 import XmlToDict


def test_simple_case():
    text = "<root>1</root>"
    etree_element = ElementTree.fromstring(text)
    expected_result = {'root': '1'}
    result = XmlToDict(etree_element).get_dict()
    assert result == expected_result, result


def test_simple_nested_case():
    text = "<root><node>1</node></root>"
    etree_element = ElementTree.fromstring(text)
    expected_result = {'root': {'node': '1'}}
    result = XmlToDict(etree_element).get_dict()
    assert result == expected_result, result


def test_simple_multi_different_nested_case():
    text = "<root><node1>1</node1><node2>2</node2></root>"
    etree_element = ElementTree.fromstring(text)
    expected_result = {'root': {'node1': '1', 'node2': '2'}}
    result = XmlToDict(etree_element).get_dict()
    assert result == expected_result, result


def test_simple_multi_same_nested_case():
    text = "<root><node>1</node><node>2</node></root>"
    etree_element = ElementTree.fromstring(text)
    expected_result = {'root': {'node': ['1', '2']}}
    result = XmlToDict(etree_element).get_dict()
    assert result == expected_result, result


def test_simple_multi_mixed_nested_case():
    text = "<root><node>1</node><node1>33</node1><node>2</node></root>"
    etree_element = ElementTree.fromstring(text)
    expected_result = {'root': {'node': ['1', '2'], 'node1': '33'}}
    result = XmlToDict(etree_element).get_dict()
    assert result == expected_result, result


def test_simple_case_with_attribute():
    text = "<root attr='attr_value1'>1</root>"
    etree_element = ElementTree.fromstring(text)
    expected_result = {'root': {'#text': '1', '@attr': 'attr_value1'}}
    result = XmlToDict(etree_element).get_dict()
    assert result == expected_result, result


def test_simple_case_with_attributes():
    text = "<root attr='attr_value1' attr2='attr_value2'>1</root>"
    etree_element = ElementTree.fromstring(text)
    expected_result = {'root': {'#text': '1',
                                '@attr': 'attr_value1',
                                '@attr2': 'attr_value2'}}
    result = XmlToDict(etree_element).get_dict()
    assert result == expected_result, result


def test_nested_case_with_attributes():
    text = "<root attr='attr_value1' attr2='attr_value2'><node>1</node></root>"
    etree_element = ElementTree.fromstring(text)
    expected_result = {'root': {'node': '1',
                                '@attr': 'attr_value1',
                                '@attr2': 'attr_value2'}}
    result = XmlToDict(etree_element).get_dict()
    assert result == expected_result, result


def test_nested_case_with_attributes_2():
    text = "<root><node attr='attr_value1' attr2='attr_value2'>1</node></root>"
    etree_element = ElementTree.fromstring(text)
    expected_result = {'root': {'node': {
        '#text': '1', '@attr': 'attr_value1', '@attr2': 'attr_value2'}}}
    result = XmlToDict(etree_element).get_dict()
    assert result == expected_result, result


def test_mixed_nested_case_with_attributes_2():
    text = "<root><node attr='attr_value1' attr2='attr_value2'>1</node>" \
           "<node>3</node></root>"
    etree_element = ElementTree.fromstring(text)
    expected_result = {'root': {'node': [{
        '#text': '1', '@attr': 'attr_value1', '@attr2': 'attr_value2'}, '3']}}
    result = XmlToDict(etree_element).get_dict()
    assert result == expected_result, result


def test_mixed_nested_case_with_attributes_3():
    text = "<root attr=\"attr_val\">" \
           "<node attr='attr_value1' attr2='attr_value2'>1</node>" \
           "<node>3</node></root>"
    etree_element = ElementTree.fromstring(text)
    expected_result = {'root': {'@attr': 'attr_val', 'node': [{
        '#text': '1', '@attr': 'attr_value1', '@attr2': 'attr_value2'}, '3']}}
    result = XmlToDict(etree_element).get_dict()
    assert result == expected_result, result


def test_simple_case_with_namespace():
    text = '<root xmlns="http://test.com/test_shema">1</root>'
    etree_element = ElementTree.fromstring(text)
    expected_result = {'root': '1'}
    result = XmlToDict(etree_element, ignore_namespace=True).get_dict()
    assert result == expected_result, result


def test_multi_different_nested_case_with_namespace():
    text = '<root xmlns="http://test.com/test_shema">' \
           '<node1>1</node1><node2>2</node2></root>'
    etree_element = ElementTree.fromstring(text)
    expected_result = {'root': {'node1': '1', 'node2': '2'}}
    result = XmlToDict(etree_element, ignore_namespace=True).get_dict()
    assert result == expected_result, result


def test_mixed_nested_case_with_attributes_with_namespace():
    text = "<root attr=\"attr_val\" xmlns=\"http://test.com/test_shema\">" \
           "<node attr='attr_value1' attr2='attr_value2'>1</node>" \
           "<node>3</node></root>"
    etree_element = ElementTree.fromstring(text)
    expected_result = {'root': {'@attr': 'attr_val', 'node': [{
        '#text': '1', '@attr': 'attr_value1', '@attr2': 'attr_value2'}, '3']}}
    result = XmlToDict(etree_element, ignore_namespace=True).get_dict()
    assert result == expected_result, result


####
def test_empty_element():
    text = "<root><node>1</node><node /></root>"
    etree_element = ElementTree.fromstring(text)
    expected_result = {'root': {'node': ['1', None]}}
    result = XmlToDict(etree_element).get_dict()
    assert result == expected_result, result


def test_tag_with_hyphen():
    text = "<root><node-n>1</node-n><node-n /></root>"
    etree_element = ElementTree.fromstring(text)
    expected_result = {'root': {'node-n': ['1', None]}}
    result = XmlToDict(etree_element).get_dict()
    assert result == expected_result, result
