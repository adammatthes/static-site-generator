import unittest
from textnode import TextNode, TextType
from splitdelimeter import split_nodes_delimeter

class TestSplitDelimeter(unittest.TestCase):
    def test_single_embed(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN, '')
        new_nodes = split_nodes_delimeter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual([n.text_type for n in new_nodes], [TextType.PLAIN, TextType.CODE, TextType.PLAIN])
