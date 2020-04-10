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
