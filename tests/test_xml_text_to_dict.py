from xmltodict3 import XmlTextToDict


def test_mixed_nested_case_with_attributes_with_namespace():
    text = "<root attr=\"attr_val\" xmlns=\"http://test.com/test_shema\">" \
           "<node attr='attr_value1' attr2='attr_value2'>1</node>" \
           "<node>3</node></root>"
    expected_result = {'root': {'@attr': 'attr_val', 'node': [{
        '#text': '1', '@attr': 'attr_value1', '@attr2': 'attr_value2'}, '3']}}
    result = XmlTextToDict(text, ignore_namespace=True).get_dict()
    assert result == expected_result, result
