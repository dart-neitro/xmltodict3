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

    def transform_node(self, node_data: Dict):
        if self.check_node_data(node_data):
            if self.using_default_value:
                node_data['#text'] = self.get_safe_value(node_data)
            else:
                node_data['#text'] = self.get_value(node_data)
            del node_data["@type"]
        return node_data

    def check_node_data(self, node_data: Dict):
        if node_data.get("@type") != self.key:
            return False
        if "#text" not in node_data:
            return False
        return True

    def get_safe_value(self, node_data: Dict):
        try:
            value = self.get_value(node_data)
        except TransformerException:
            value = self.default_value
        return value

    def get_value(self, node_data: Dict):
        try:
            return self.get_value_or_raise_exception(node_data)
        except Exception as e:
            raise TransformerException(str(e))

    @abstractmethod
    def get_value_or_raise_exception(self, node_data: Dict):
        pass

    def set_using_default_value(self, using_default_value: bool):
        self.using_default_value = using_default_value


class IntegerTransformer(AbstractTransformer):
    key = "integer"

    def get_value_or_raise_exception(self, node_data: Dict):
        return int(node_data['#text'])


class BoolTransformer(AbstractTransformer):
    key = "bool"

    def get_value_or_raise_exception(self, node_data: Dict):
        value = node_data['#text'].lower()
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

    def get_value_or_raise_exception(self, node_data: Dict):
        value = node_data['#text'].lower()
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

    def transform_node(self, node_data: Dict):
        key = self.get_key(node_data)
        if key is not None:
            transformer = self.get_transformer(key)
            if transformer is not None:
                return transformer.transform_node(node_data)
        return node_data

    @staticmethod
    def get_key(node_data: Dict):
        if '@type' in node_data:
            return node_data['@type']

    def get_transformer(self, key):
        if key in self.transformers:
            return self.transformers[key]
        return None

    def set_using_default_value(self, using_default_value: bool):
        for transformer_key in self.transformers:
            self.transformers[transformer_key].set_using_default_value(
                using_default_value
            )


DefaultTransformerList = [
    IntegerTransformer(), BoolTransformer(), DateTimeTransformer()]
