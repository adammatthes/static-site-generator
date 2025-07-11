import unittest

from htmlnode import HTMLNode

placeholder = "This is some text"

children_temp = HTMLNode('p', placeholder, None, None)

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode('a', placeholder, None, None)
        node2 = HTMLNode('a', placeholder, None, None)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = HTMLNode('a', placeholder, None, None)
        node2 = HTMLNode('a', placeholder[:-1], None, None)
        self.assertNotEqual(node, node2)

    def test_raise_for_no_children(self):
        with self.assertRaises(AssertionError):
            node = HTMLNode('a', None, None, None)


