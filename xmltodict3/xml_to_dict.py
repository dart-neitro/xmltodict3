from collections import defaultdict
import re
import xml.etree.ElementTree as ElementTree
from typing import Union, Dict


class XmlToDict:
    __pull_transformers = None

    def __init__(self, node: ElementTree, ignore_namespace: bool = False):
        self.node = node
        self.ignore_namespace = ignore_namespace
        self.children_nodes = []

    def get_dict(self):
        tag = self.get_tag()
        self.children_nodes = self.get_children_nodes()
        if self.is_single_node():
            value = self.get_dict_from_single_node()
        else:
            value = self.get_dict_from_node_with_children()
        return {tag: value}

    def get_tag(self):
        tag = self.node.tag
        if self.ignore_namespace:
            tag = re.sub(r'{[^}]+}', '', tag)
        return tag

    def get_children_nodes(self):
        children_nodes = []
        for child_node in self.node:
            xml_to_dict_node = XmlToDict(
                child_node, ignore_namespace=self.ignore_namespace)
            if self.__pull_transformers is not None:
                xml_to_dict_node.use_pull_transformers(
                    self.__pull_transformers)
            children_nodes.append(xml_to_dict_node)
        return children_nodes

    def is_single_node(self):
        return True if not self.children_nodes else False

    def get_dict_from_single_node(self):
        attributes = self.get_attributes()
        if attributes:
            value = attributes.copy()
            value['#text'] = self.get_value()
        else:
            value = {'#text': self.get_value()}
        value = self.transform_node(value)
        value = self.group_simple_node_data(value)
        return value

    def get_value(self) -> Union[str, None]:
        value = self.node.text
        if value is not None:
            value = value.strip()
        return value

    def transform_node(self, node_data: Dict):
        if self.__pull_transformers is not None:
            node_data = self.__pull_transformers.transform_node(node_data)
        return node_data

    def group_simple_node_data(self, node_data: Dict):
        if tuple(node_data.keys()) == ('#text',):
            node_data = node_data['#text']
        return node_data

    def get_dict_from_node_with_children(self):
        children_data = self.get_children_data()
        attributes = self.get_attributes()
        if attributes:
            value = {**children_data, **attributes}
        else:
            value = children_data
        return value

    def get_attributes(self):
        attributes = dict()
        for attribute_name in self.node.attrib:
            key = '@' + attribute_name
            attributes[key] = self.node.attrib[attribute_name]
        return attributes

    def get_children_data(self):
        node_data = defaultdict(list)
        for child_node in self.children_nodes:
            tag = child_node.get_tag()
            node_data[tag].append(child_node.get_dict()[tag])
        node_data = self.group_children_data(node_data)
        return node_data

    def group_children_data(self, children_data: defaultdict):
        grouped_data = dict()
        for tag in children_data:
            sub_node_data = children_data[tag]
            if len(sub_node_data) == 1:
                grouped_data[tag] = sub_node_data[0]
            else:
                grouped_data[tag] = sub_node_data
        return grouped_data

    def use_pull_transformers(self, pull_transformers):
        self.__pull_transformers = pull_transformers


class XmlFileToDict:
    def __init__(self, file_path: str, ignore_namespace: bool = False):
        self.file_path = file_path
        self.ignore_namespace = ignore_namespace
        self.__pull_transformers = None

    def get_dict(self):
        tree_node = ElementTree.parse(self.file_path)
        root_node = tree_node.getroot()
        xml_to_dict_node = XmlToDict(
            root_node, ignore_namespace=self.ignore_namespace)
        if self.__pull_transformers is not None:
            xml_to_dict_node.use_pull_transformers(
                self.__pull_transformers)
        return xml_to_dict_node.get_dict()

    def use_pull_transformers(self, pull_transformers):
        self.__pull_transformers = pull_transformers


class XmlTextToDict:
    def __init__(self, xml_text: str, ignore_namespace: bool = False):
        self.xml_text = xml_text
        self.ignore_namespace = ignore_namespace
        self.__pull_transformers = None

    def get_dict(self):
        root_node = ElementTree.fromstring(self.xml_text)
        xml_to_dict_node = XmlToDict(
            root_node, ignore_namespace=self.ignore_namespace)
        if self.__pull_transformers is not None:
            xml_to_dict_node.use_pull_transformers(
                self.__pull_transformers)
        return xml_to_dict_node.get_dict()

    def use_pull_transformers(self, pull_transformers):
        self.__pull_transformers = pull_transformers
