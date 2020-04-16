"""
Implementing and using a custom transformer
"""
import xml.etree.ElementTree as ElementTree
from typing import Dict
from decimal import Decimal

from xmltodict3 import (
    XmlToDict, PullTransformers)

from xmltodict3.transformers import AbstractTransformer


class DecimalTransformer(AbstractTransformer):
    key = "decimal"

    def get_value_or_raise_exception(self, node_data: Dict):
        return Decimal(node_data['#text'])


text = """
<tag_decimal type="decimal">
    1500.00
</tag_decimal>
"""


expected_result = {'tag_decimal': Decimal(1500.00)}

custom_transformer_list = [DecimalTransformer()]
pull_transformers = PullTransformers(*custom_transformer_list)

etree_element = ElementTree.fromstring(text)
xmt_to_dict = XmlToDict(etree_element)
xmt_to_dict.use_pull_transformers(pull_transformers)

result = xmt_to_dict.get_dict()

assert result == expected_result, result
