from abc import ABC, abstractmethod
from typing import Dict


class TransformerException(Exception):
    pass


class AbstractTransformer(ABC):
    """
    transformation for data node
    """
    key = None
    default_value = None
    using_default_value = True

    def transform_node(self, data_node: Dict):
        if self.check_data_node(data_node):
            if self.using_default_value:
                data_node['#text'] = self.get_safe_value(data_node)
            else:
                data_node['#text'] = self.get_value(data_node)
            del data_node["@type"]
        return data_node

    def check_data_node(self, data_node: Dict):
        if data_node.get("@type") != self.key:
            return False
        if "#text" not in data_node:
            return False
        return True

    def get_key(self):
        return self.key

    def get_safe_value(self, data_node: Dict):
        try:
            value = self.get_value(data_node)
        except TransformerException:
            value = self.default_value
        return value

    def get_value(self, data_node: Dict):
        try:
            return self._get_value(data_node)
        except Exception as e:
            raise TransformerException(str(e))

    @abstractmethod
    def _get_value(self, data_node: Dict):
        pass


class IntegerTransformer(AbstractTransformer):
    key = "integer"

    def _get_value(self, data_node: Dict):
        return int(data_node['#text'])


class BoolTransformer(AbstractTransformer):
    key = "bool"

    def _get_value(self, data_node: Dict):
        value = data_node['#text'].lower()
        if value == 'true':
            value = True
        elif value == 'false':
            value = False
        else:
            raise TypeError('Value has to be "true" or "false"')
        return value
