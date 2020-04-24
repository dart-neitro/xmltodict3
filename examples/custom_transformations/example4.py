"""
Case with invalid data
"""
from decimal import Decimal
import re
from typing import Dict

from xmltodict3 import (
    XmlFileToDict, DefaultTransformerList, PullTransformers)
from xmltodict3.transformers import AbstractTransformer


transformer_list = DefaultTransformerList
xml_to_dict = XmlFileToDict(file_path='data/ex4.xml')

expected_result = {
    'breakfast_menu': {
        'food': [
            {
                'name': 'Belgian Waffles',
                'price': {'@type': 'price', '#text': '$5.95'},
                'description': 'Two of our famous Belgian Waffles'
                               ' with plenty of real maple syrup',
                'calories': {'@type': 'integer', '#text': '650'},
                'discount': {'@type': 'discount', '#text': '15%'}
            },
            {
                'name': 'Strawberry Belgian Waffles',
                'price': {'@type': 'price', '#text': '$7.95'},
                'description': 'Light Belgian waffles covered with '
                               'strawberries and whipped cream',
                'calories': {'@type': 'integer', '#text': '900'},
                'discount': {'@type': 'discount', '#text': '10.5%'}
            }
        ]
    }
}
result = xml_to_dict.get_dict()
assert result == expected_result, result


class PriceTransformer(AbstractTransformer):
    key = "price"

    def get_value_or_raise_exception(self, node_data: Dict):
        value = node_data['#text']
        pattern = r'^\$(\d+\.?\d*)$'
        pattern_match = re.match(pattern, value)
        if not pattern_match:
            raise TypeError(
                f'The value <{repr(value)}> '
                f'has not matched with pattern <{pattern}>')
        value = pattern_match.group(1)
        return Decimal(value)


class DiscountTransformer(AbstractTransformer):
    key = "discount"

    def get_value_or_raise_exception(self, node_data: Dict):
        value = node_data['#text']
        pattern = r'^(\d+\.?\d*)\%$'
        pattern_match = re.match(pattern, value)
        if not pattern_match:
            raise TypeError(
                f'The value <{repr(value)}> '
                f'has not matched with pattern <{pattern}>')
        value = pattern_match.group(1)
        return Decimal(value)


custom_transformer_list = [PriceTransformer, DiscountTransformer]
custom_transformer_list = transformer_list + custom_transformer_list
pull_transformers = PullTransformers(*custom_transformer_list)
pull_transformers.set_removing_types(True)
xml_to_dict.use_pull_transformers(pull_transformers)


expected_result = {
    'breakfast_menu': {
        'food': [
            {
                'calories': 650,
                'description': 'Two of our famous Belgian Waffles '
                               'with plenty of real maple syrup',
                'name': 'Belgian Waffles',
                'price': Decimal('5.95'),
                'discount': Decimal('15'),
            },
            {
                'calories': 900,
                'description': 'Light Belgian waffles covered '
                               'with strawberries and whipped cream',
                'name': 'Strawberry Belgian Waffles',
                'price': Decimal('7.95'),
                'discount': Decimal('10.5'),
            }
        ]
    }
}

result = xml_to_dict.get_dict()
assert result == expected_result, result
