"""
Using custom transformer plus default transformers
"""
import datetime
import xml.etree.ElementTree as ElementTree
from typing import Dict
from decimal import Decimal

from xmltodict3 import (
    XmlToDict, DefaultTransformerList, PullTransformers)

from xmltodict3.transformers import AbstractTransformer


class DecimalTransformer(AbstractTransformer):
    key = "decimal"

    def get_value_or_raise_exception(self, node_data: Dict):
        return Decimal(node_data['#text'])


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
        <tag_decimal type="decimal">
            1500.00
        </tag_decimal>
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
    'tag_decimal': Decimal(1500.00)
}}}

custom_transformer_list = [DecimalTransformer]
transformer_list = DefaultTransformerList + custom_transformer_list
pull_transformers = PullTransformers(*transformer_list)
pull_transformers.set_removing_types(True)

etree_element = ElementTree.fromstring(text)
xml_to_dict = XmlToDict(etree_element)
xml_to_dict.use_pull_transformers(pull_transformers)

result = xml_to_dict.get_dict()

assert result == expected_result, result
