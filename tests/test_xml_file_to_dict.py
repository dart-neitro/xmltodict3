import os

from xmltodict3 import XmlFileToDict


SAMPLE_FOOD_DICT = {
        'breakfast_menu': {
            'food': [
                {
                    'calories': '650',
                    'description': 'Two of our famous Belgian '
                    'Waffles with plenty of real '
                    'maple syrup',
                    'name': 'Belgian Waffles',
                    'price': '$5.95'
                },
                {
                    'calories': '900',
                    'description': 'Light Belgian waffles covered '
                    'with strawberries and whipped '
                    'cream',
                    'name': 'Strawberry Belgian Waffles',
                    'price': '$7.95'
                },
                {
                    'calories': '900',
                    'description': 'Light Belgian waffles covered '
                    'with an assortment of fresh '
                    'berries and whipped cream',
                    'name': 'Berry-Berry Belgian Waffles',
                    'price': '$8.95'
                },
                {
                    'calories': '600',
                    'description': 'Thick slices made from our '
                    'homemade sourdough bread',
                    'name': 'French Toast',
                    'price': '$4.50'
                },
                {
                    'calories': '950',
                    'description': 'Two eggs, bacon or sausage, '
                    'toast, and our ever-popular hash '
                    'browns',
                    'name': 'Homestyle Breakfast',
                    'price': '$6.95'
                }]
        }
    }


def test_simple_case():
    current_path = os.path.dirname(os.path.abspath(__file__))
    sample_xml_file_path = os.path.join(
        current_path, 'test_data/sample_food.xml')
    result = XmlFileToDict(sample_xml_file_path).get_dict()
    expected_result = SAMPLE_FOOD_DICT
    assert result == expected_result, result


def test_simple_case_with_name_space():
    current_path = os.path.dirname(os.path.abspath(__file__))
    sample_xml_file_path = os.path.join(
        current_path, 'test_data/sample_food_with_namespace.xml')
    result = XmlFileToDict(
        sample_xml_file_path, ignore_namespace=True).get_dict()
    expected_result = SAMPLE_FOOD_DICT
    assert result == expected_result, result
