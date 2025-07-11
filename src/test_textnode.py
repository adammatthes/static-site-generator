import unittest

from textnode import TextNode, TextType

placeholder = "This is a text node"
url = 'www.example.com'

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode(placeholder, TextType.BOLD, url)
        node2 = TextNode(placeholder, TextType.BOLD, url)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode(placeholder, TextType.ITALIC, url)
        node2 = TextNode(placeholder, TextType.LINK, url)
        self.assertNotEqual(node, node2)

    def test_none_url(self):
        node = TextNode(placeholder, TextType.BOLD, url)
        node2 = TextNode(placeholder, TextType.BOLD, None)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
