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

    def get_children_data(self):
        node_data = {}
        for child_node in self.children_nodes:
            tag = child_node.get_tag()
            node_data[tag] = child_node.get_dict()[tag]
        return node_data

    def get_tag(self):
        return self.node.tag
