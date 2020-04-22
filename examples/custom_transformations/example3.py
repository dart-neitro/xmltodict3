"""
Case with invalid data
"""


from xmltodict3 import (
    XmlTextToDict, DefaultTransformerList,
    PullTransformers, TransformerException)


text = """
<root>
    <values>
        <int_value type="integer">
            $42
        </int_value>
    </values>
</root>
"""

transformer_list = DefaultTransformerList
pull_transformers = PullTransformers(*transformer_list)

xml_to_dict = XmlTextToDict(xml_text=text)
xml_to_dict.use_pull_transformers(pull_transformers)

try:
    xml_to_dict.get_dict()
except TransformerException:
    pass
else:
    raise Exception('TransformerException has not raised')
