import xml.etree.ElementTree as ElementTree

from xmltodict3 import XmlToDict


def test_simple_case():
    text = "<root>1</root>"
    etree_element = ElementTree.fromstring(text)
    expected_result = {'root': '1'}
    result = XmlToDict(etree_element).get_dict()
    assert result == expected_result, result
