import unittest
from textnode import TextNode, TextType
from splitdelimeter import split_nodes_delimeter

class TestSplitDelimeter(unittest.TestCase):
    def test_single_embed(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN, '')
        new_nodes = split_nodes_delimeter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual([n.text_type for n in new_nodes], [TextType.PLAIN, TextType.CODE, TextType.PLAIN])

    def test_two_embed(self):
        node = TextNode("This is _text_ with a **bold** word", TextType.PLAIN, '')
        temp_nodes = split_nodes_delimeter([node],  "**", TextType.BOLD)
        print(temp_nodes)
        new_nodes = split_nodes_delimeter(temp_nodes, "_", TextType.ITALIC)
        print(new_nodes)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual([n.text_type for n in new_nodes], [TextType.PLAIN, TextType.ITALIC, TextType.PLAIN, TextType.BOLD, TextType.PLAIN])
