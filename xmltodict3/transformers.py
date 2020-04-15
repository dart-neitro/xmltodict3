from abc import ABC, abstractmethod
import datetime
from typing import Dict


class TransformerException(Exception):
    pass


class AbstractTransformer(ABC):
    """
    transformation for data node
    """
    key = None

    def __init__(self, default_value=None, using_default_value: bool = True):
        self.default_value = default_value
        self.using_default_value = using_default_value

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

    def get_safe_value(self, data_node: Dict):
        try:
            value = self.get_value(data_node)
        except TransformerException:
            value = self.default_value
        return value

    def get_value(self, data_node: Dict):
        try:
            return self.get_value_or_raise_exception(data_node)
        except Exception as e:
            raise TransformerException(str(e))

    @abstractmethod
    def get_value_or_raise_exception(self, data_node: Dict):
        pass


class IntegerTransformer(AbstractTransformer):
    key = "integer"

    def get_value_or_raise_exception(self, data_node: Dict):
        return int(data_node['#text'])


class BoolTransformer(AbstractTransformer):
    key = "bool"

    def get_value_or_raise_exception(self, data_node: Dict):
        value = data_node['#text'].lower()
        if value == 'true':
            value = True
        elif value == 'false':
            value = False
        else:
            raise TypeError('Value has to be "true" or "false"')
        return value


class DateTimeTransformer(AbstractTransformer):
    key = "datetime"
    datetime_format = "%Y-%m-%dT%H:%M:%SZ"

    def get_value_or_raise_exception(self, data_node: Dict):
        value = data_node['#text'].lower()
        value = datetime.datetime.strptime(value, self.datetime_format)
        return value

    def set_datetime_format(self, datetime_format: str):
        self.datetime_format = datetime_format


class PullTransformers:
    def __init__(self, *transformers):
        self.transformers = dict()
        self.add_transformers(*transformers)

    def add_transformers(self, *transformers):
        for transformer in transformers:
            self.__register_transformer(transformer)

    def __register_transformer(self, transformer: AbstractTransformer):
        if issubclass(transformer.__class__, AbstractTransformer):
            self.transformers[transformer.key] = transformer

    def transform_node(self, data_node: Dict):
        key = self.get_key(data_node)
        if key is not None:
            transformer = self.get_transformer(key)
            if transformer is not None:
                return transformer.transform_node(data_node)
        return data_node

    @staticmethod
    def get_key(data_node: Dict):
        if '@type' in data_node:
            return data_node['@type']

    def get_transformer(self, key):
        if key in self.transformers:
            return self.transformers[key]
        return None


DefaultTransformerList = [
    IntegerTransformer(), BoolTransformer(), DateTimeTransformer()]
