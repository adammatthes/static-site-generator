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
        new_nodes = split_nodes_delimeter(temp_nodes, "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual([n.text_type for n in new_nodes], [TextType.PLAIN, TextType.ITALIC, TextType.PLAIN, TextType.BOLD, TextType.PLAIN])

    def test_image_extract(self):
        node = TextNode("Check out ![my dog](www.cuteanimals.com)", TextType.PLAIN, '')
        new_nodes = split_nodes_delimeter([node], '!', TextType.IMAGE)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual([n.text_type for n in new_nodes], [TextType.PLAIN, TextType.IMAGE])

    def test_link_extract(self):
        node = TextNode("Follow my socials [here](www.link.tr)", TextType.PLAIN, '')
        new_nodes = split_nodes_delimeter([node], '[', TextType.LINK)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual([n.text_type for n in new_nodes], [TextType.PLAIN, TextType.LINK])
