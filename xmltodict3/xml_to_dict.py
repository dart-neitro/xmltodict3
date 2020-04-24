from collections import defaultdict
import re
import xml.etree.ElementTree as ElementTree
from typing import Union, Dict, List

from xmltodict3.transformers import PullTransformers


class XmlToDict:
    """Class to work with xml.etree.ElementTree objects"""
    _pull_transformers = None

    def __init__(self, node: ElementTree, ignore_namespace: bool = False):
        self.node = node
        self.ignore_namespace = ignore_namespace
        self.children_nodes = list()

    def get_dict(self) -> Dict:
        tag = self.get_tag()
        self.children_nodes = self._get_children_nodes()
        if self._is_single_node():
            value = self._get_dict_from_single_node()
        else:
            value = self._get_dict_from_node_with_children()
        return {tag: value}

    def get_tag(self) -> str:
        tag = self.node.tag
        if self.ignore_namespace:
            tag = re.sub(r'{[^}]+}', '', tag)
        return tag

    def _get_children_nodes(self) -> List:
        children_nodes = []
        for child_node in self.node:
            xml_to_dict_node = XmlToDict(
                child_node, ignore_namespace=self.ignore_namespace)
            if self._pull_transformers is not None:
                xml_to_dict_node.use_pull_transformers(
                    self._pull_transformers)
            children_nodes.append(xml_to_dict_node)
        return children_nodes

    def _is_single_node(self) -> bool:
        return True if not self.children_nodes else False

    def _get_dict_from_single_node(self) -> Dict:
        data_node = self._get_simple_data_node()
        transformed_data_node = self._transform_node(data_node)
        grouped_data_node = self._group_simple_node_data(transformed_data_node)
        return grouped_data_node

    def _get_simple_data_node(self) -> Dict:
        attributes = self._get_attributes()
        node_value = {'#text': self._get_value()}
        data_node = {**attributes, **node_value}
        return data_node

    def _get_value(self) -> Union[str, None]:
        value = self.node.text
        if value is not None:
            value = value.strip()
        return value

    def _transform_node(self, node_data: Dict) -> Dict:
        if self._pull_transformers is not None:
            node_data = self._pull_transformers.transform_node(node_data)
        return node_data

    @staticmethod
    def _group_simple_node_data(node_data: Dict) -> Dict:
        if tuple(node_data.keys()) == ('#text',):
            node_data = node_data['#text']
        return node_data

    def _get_dict_from_node_with_children(self) -> Dict:
        attributes = self._get_attributes()
        children_data = self._get_children_data()
        value = {**children_data, **attributes}
        return value

    def _get_attributes(self) -> Dict:
        attributes = dict()
        for attribute_name in self.node.attrib:
            key = '@' + attribute_name
            attributes[key] = self.node.attrib[attribute_name]
        return attributes

    def _get_children_data(self) -> Dict:
        node_data = defaultdict(list)
        for child_node in self.children_nodes:
            tag = child_node.get_tag()
            node_data[tag].append(child_node.get_dict()[tag])
        node_data = self._group_children_data(node_data)
        return node_data

    @staticmethod
    def _group_children_data(children_data: defaultdict) -> Dict:
        grouped_data = dict()
        for tag in children_data:
            sub_node_data = children_data[tag]
            if len(sub_node_data) == 1:
                grouped_data[tag] = sub_node_data[0]
            else:
                grouped_data[tag] = sub_node_data
        return grouped_data

    def use_pull_transformers(
            self, pull_transformers: PullTransformers) -> None:
        if isinstance(pull_transformers, PullTransformers):
            self._pull_transformers = pull_transformers


class XmlTextToDict:
    """Class to work with strings which contain XML"""
    def __init__(self, xml_text: str, ignore_namespace: bool = False):
        self.xml_text = xml_text
        self.ignore_namespace = ignore_namespace
        self._pull_transformers = None

    def get_dict(self) -> Dict:
        xml_to_dict_node = self.get_xml_to_dict_node()
        if self._pull_transformers is not None:
            xml_to_dict_node.use_pull_transformers(
                self._pull_transformers)
        return xml_to_dict_node.get_dict()

    def get_xml_to_dict_node(self) -> XmlToDict:
        root_node = ElementTree.fromstring(self.xml_text)
        xml_to_dict_node = XmlToDict(
            root_node, ignore_namespace=self.ignore_namespace)
        return xml_to_dict_node

    def use_pull_transformers(
            self, pull_transformers: PullTransformers) -> None:
        if isinstance(pull_transformers, PullTransformers):
            self._pull_transformers = pull_transformers


class XmlFileToDict(XmlTextToDict):
    """Class to work with XML files"""
    def __init__(self, file_path: str, ignore_namespace: bool = False):
        self.file_path = file_path
        self.ignore_namespace = ignore_namespace
        self._pull_transformers = None

    def get_xml_to_dict_node(self) -> XmlToDict:
        tree_node = ElementTree.parse(self.file_path)
        root_node = tree_node.getroot()
        xml_to_dict_node = XmlToDict(
            root_node, ignore_namespace=self.ignore_namespace)
        return xml_to_dict_node
