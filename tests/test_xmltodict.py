import xml.etree.ElementTree as ElementTree


def test_simple_case():
    text = "<root>1</root>"
    etree_element = ElementTree.fromstring(text)
    expected_result = {'root': '1'}
    result = None
    assert result == expected_result, result
