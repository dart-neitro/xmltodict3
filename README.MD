An open-source library that is used for converting XML to a python dictionary.

This library:
* work with namespace
* can transform XML value into python object (integer, boolean, datetime & custom transformers) using the "type" attribute

Example 1 (Simple case):
-------
    >>> from xmltodict3 import XmlTextToDict
    >>> text = """
    ...     <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
    ...         <xs:root attr="attr_value">
    ...             data
    ...         </xs:root>
    ...     </xs:schema>
    ... """
    >>> result = XmlTextToDict(text, ignore_namespace=True).get_dict()
    >>> print(result)
    {'schema': {'root': {'@attr': 'attr_value', '#text': 'data'}}}

Example 2 (with transformers):
---------
    
    >>> from xmltodict3 import XmlTextToDict
    >>> import xmltodict3.transformers as transformers
    >>> text = """
    ... <root>
    ...     <values>
    ...         <int_value type="integer">
    ...             123
    ...         </int_value>
    ...     </values>
    ... </root>
    ... """
    >>> transformer_list = transformers.DefaultTransformerList
    >>> pull_transformers = transformers.PullTransformers(*transformer_list)
    >>> pull_transformers.set_removing_types(True)
    >>> xml_to_dict = XmlTextToDict(text)
    >>> xml_to_dict.use_pull_transformers(pull_transformers)
    >>> result = xml_to_dict.get_dict()
    >>> print(result)
    {'root': {'values': {'int_value': 123}}}

# [More examples](https://github.com/dart-neitro/xmltodict3/tree/master/examples)


