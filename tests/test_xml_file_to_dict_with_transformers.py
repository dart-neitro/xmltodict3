import os
import re
from decimal import Decimal
from typing import Dict

from xmltodict3 import XmlFileToDict
import xmltodict3.transformers as transformers


SAMPLE_FOOD_DICT = {
        'breakfast_menu': {
            'food': [
                {
                    'calories': 650,
                    'description': 'Two of our famous Belgian '
                    'Waffles with plenty of real '
                    'maple syrup',
                    'name': 'Belgian Waffles',
                    'price': Decimal('5.95'),
                },
                {
                    'calories': 900,
                    'description': 'Light Belgian waffles covered '
                    'with strawberries and whipped '
                    'cream',
                    'name': 'Strawberry Belgian Waffles',
                    'price': Decimal('7.95'),
                },
                {
                    'calories': 900,
                    'description': 'Light Belgian waffles covered '
                    'with an assortment of fresh '
                    'berries and whipped cream',
                    'name': 'Berry-Berry Belgian Waffles',
                    'price': Decimal('8.95'),
                },
                {
                    'calories': 600,
                    'description': 'Thick slices made from our '
                    'homemade sourdough bread',
                    'name': 'French Toast',
                    'price': Decimal('4.50'),
                },
                {
                    'calories': 950,
                    'description': 'Two eggs, bacon or sausage, '
                    'toast, and our ever-popular hash '
                    'browns',
                    'name': 'Homestyle Breakfast',
                    'price': Decimal('6'),
                }]
        }
    }


class PriceTransformer(transformers.AbstractTransformer):
    key = "price"

    def get_value_or_raise_exception(self, node_data: Dict):
        value = node_data['#text']
        pattern_match = re.match(r'^\$(\d+\.?\d*)$', value)
        if not pattern_match:
            raise TypeError
        value = pattern_match.group(1)
        return Decimal(value)


def test_xml_file_with_pull_transformers():
    current_path = os.path.dirname(os.path.abspath(__file__))
    sample_xml_file_path = os.path.join(
        current_path, 'test_data/sample_food_with_types.xml')

    transformer_list = transformers.DefaultTransformerList
    transformer_list += [PriceTransformer]
    pull_transformers = transformers.PullTransformers(*transformer_list)
    pull_transformers.set_removing_types(True)

    xml_to_dict = XmlFileToDict(sample_xml_file_path)
    xml_to_dict.use_pull_transformers(pull_transformers)

    result = xml_to_dict.get_dict()
    expected_result = SAMPLE_FOOD_DICT
    assert result == expected_result, result
