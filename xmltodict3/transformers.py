"""
Classes to work with transformation data
during transformation from XML to python dictionary
"""
from abc import ABC, abstractmethod
import datetime
from typing import Dict, Any, Optional, Union

from xmltodict3.exceptions import TransformerException


class AbstractTransformer(ABC):
    """Abstract class for implementation transformers"""
    key = None

    def __init__(self, ignore_errors: bool = False,
                 removing_types: bool = False):
        self.ignore_errors = ignore_errors
        self.removing_types = removing_types

    def transform_node(self, node_data: Dict) -> Dict:
        if self.check_node_data(node_data):
            if self.ignore_errors:
                node_data['#text'] = self.get_safe_value(node_data)
            else:
                node_data['#text'] = self.get_value(node_data)
            node_data = self.remove_type_from_node_data(node_data)
        return node_data

    def check_node_data(self, node_data: Dict) -> bool:
        if node_data.get("@type") != self.key:
            return False
        if "#text" not in node_data:
            return False
        return True

    def get_safe_value(self, node_data: Dict) -> Any:
        try:
            value = self.get_value(node_data)
        except TransformerException:
            value = node_data.get("#text")
        return value

    def get_value(self, node_data: Dict) -> Any:
        try:
            return self.get_value_or_raise_exception(node_data)
        except Exception as e:
            raise TransformerException(
                '{0}: {1}'.format(self.__class__, str(e)))

    @abstractmethod
    def get_value_or_raise_exception(self, node_data: Dict) -> Any:
        pass

    def remove_type_from_node_data(self, node_data: Dict) -> Dict:
        if self.removing_types:
            del node_data["@type"]
        return node_data

    def set_ignore_errors(self, ignore_errors: bool) -> None:
        self.ignore_errors = ignore_errors

    def set_removing_types(self, removing_types: bool) -> None:
        self.removing_types = removing_types


class IntegerTransformer(AbstractTransformer):
    """Transformer for integers"""
    key = "integer"

    def get_value_or_raise_exception(self, node_data: Dict) -> int:
        return int(node_data['#text'])


class BoolTransformer(AbstractTransformer):
    """Transformer for booleans"""
    key = "bool"

    def get_value_or_raise_exception(self, node_data: Dict) -> bool:
        value = node_data['#text'].lower()
        if value == 'true':
            value = True
        elif value == 'false':
            value = False
        else:
            raise TypeError('Value has to be "true" or "false"')
        return value


class DateTimeTransformer(AbstractTransformer):
    """Transformer for datetime.datetime"""
    key = "datetime"
    datetime_format = "%Y-%m-%dT%H:%M:%SZ"

    def get_value_or_raise_exception(
            self, node_data: Dict) -> datetime.datetime:
        value = node_data['#text'].lower()
        value = datetime.datetime.strptime(value, self.datetime_format)
        return value

    def set_datetime_format(self, datetime_format: str) -> None:
        self.datetime_format = datetime_format


class PullTransformers:
    def __init__(self, *transformers):
        self.transformers = dict()
        self.add_transformers(*transformers)

    def add_transformers(self, *transformers) -> None:
        for transformer in transformers:
            self.__register_transformer(transformer)

    def __register_transformer(
            self, transformer: Union[AbstractTransformer, type]) -> None:
        transformer_instance = self.__get_transformer_instance(transformer)
        if issubclass(transformer_instance.__class__, AbstractTransformer):
            self.transformers[transformer_instance.key] = transformer_instance

    @staticmethod
    def __get_transformer_instance(
            transformer: Union[AbstractTransformer, type]
            ) -> AbstractTransformer:
        if issubclass(transformer.__class__, type):
            return transformer()
        return transformer

    def transform_node(self, node_data: Dict) -> Dict:
        key = self.get_key(node_data)
        if key is not None:
            transformer = self.get_transformer(key)
            if transformer is not None:
                return transformer.transform_node(node_data)
        return node_data

    @staticmethod
    def get_key(node_data: Dict) -> Optional[str]:
        if '@type' in node_data:
            return node_data['@type']

    def get_transformer(self, key: str) -> Optional[AbstractTransformer]:
        if key in self.transformers:
            return self.transformers[key]
        return None

    def set_ignore_errors(self, ignore_errors: bool) -> None:
        for transformer_key in self.transformers:
            self.transformers[transformer_key].set_ignore_errors(
                ignore_errors
            )

    def set_removing_types(self, removing_types: bool) -> None:
        for transformer_key in self.transformers:
            self.transformers[transformer_key].set_removing_types(
                removing_types
            )


DefaultTransformerList = [
    IntegerTransformer, BoolTransformer, DateTimeTransformer]
