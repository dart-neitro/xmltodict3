from collections import defaultdict
import xml.etree.ElementTree as ElementTree


class XmlToDict:
    def __init__(self, node: ElementTree):
        self.node = node
        self.children_nodes = [XmlToDict(child_node) for child_node in node]

    def get_dict(self):
        tag = self.get_tag()
        if self.children_nodes:
            children_data = self.get_children_data()
            attributes = self.get_attributes()
            if attributes:
                value = {**children_data, **attributes}
            else:
                value = children_data
        else:
            attributes = self.get_attributes()
            if attributes:
                value = attributes.copy()
                value['#text'] = self.node.text
            else:
                value = self.node.text
        return {tag: value}

    def get_tag(self):
        return self.node.tag

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

    def group_children_data(self, children_data):
        grouped_data = dict()
        for tag in children_data:
            sub_node_data = children_data[tag]
            if len(sub_node_data) == 1:
                grouped_data[tag] = sub_node_data[0]
            else:
                grouped_data[tag] = sub_node_data
        return grouped_data

