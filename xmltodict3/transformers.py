from abc import ABC, abstractmethod
from typing import Dict


class AbstractTransformer(ABC):
    """
    transformation for data node
    """
    key = None

    @abstractmethod
    def transform_node(self, data_node: Dict):
        pass

    def check_data_node(self, data_node: Dict):
        if data_node.get("@type") != self.key:
            return False
        if "#text" not in data_node:
            return False
        return True

    def get_key(self):
        return self.key


class IntegerTransformer(AbstractTransformer):
    key = "integer"

    def transform_node(self, data_node: Dict):
        if self.check_data_node(data_node):
            data_node['#text'] = int(data_node['#text'])
            del data_node["@type"]
        return data_node


class BoolTransformer(AbstractTransformer):
    key = "bool"

    def transform_node(self, data_node: Dict):
        if self.check_data_node(data_node):
            value = data_node['#text'].lower()
            if value == 'true':
                data_node['#text'] = True
            else:
                data_node['#text'] = False
            del data_node["@type"]
        return data_node
