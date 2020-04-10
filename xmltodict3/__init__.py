import xml.etree.ElementTree as ElementTree


class XmlToDict:
    def __init__(self, node: ElementTree):
        self.node = node

    def get_dict(self):
        tag = self.node.tag
        value = self.node.text
        return {tag: value}
