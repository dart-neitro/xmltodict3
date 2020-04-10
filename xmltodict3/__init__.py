from collections import defaultdict
import xml.etree.ElementTree as ElementTree


class XmlToDict:
    def __init__(self, node: ElementTree):
        self.node = node
        self.children_nodes = [XmlToDict(child_node) for child_node in node]

    def get_dict(self):
        tag = self.get_tag()
        if self.children_nodes:
            value = self.get_children_data()
        else:
            value = self.node.text
        return {tag: value}

    def get_tag(self):
        return self.node.tag

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

