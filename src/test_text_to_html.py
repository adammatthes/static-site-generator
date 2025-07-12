import unittest
from text_to_html import text_node_to_html
from textnode import TextNode, TextType

placeholder = "This is a text node"

class TestTextNodeToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode(placeholder, TextType.PLAIN, '')
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, placeholder)

    def test_bold(self):
        node = TextNode(placeholder, TextType.BOLD, '')
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, placeholder)

    def test_italic(self):
        node = TextNode(placeholder, TextType.ITALIC, '')
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, placeholder)

    def test_code(self):
        node = TextNode(placeholder, TextType.CODE, '')
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, placeholder)

    def test_link(self):
        node = TextNode(placeholder, TextType.LINK, 'www.example.com')
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, placeholder)
        self.assertEqual(html_node.props, {'href': 'www.example.com'})

    def test_image(self):
        node = TextNode(placeholder, TextType.IMAGE, 'www.imgsrc.com')
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props, {'src':'www.imgsrc.com', 'alt':placeholder})
