import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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


class TestLeafNode(unittest.TestCase):
    def test_invalid_leaf(self):
        with self.assertRaises(ValueError):
            node = LeafNode('a', placeholder, [children_temp], None)

        with self.assertRaises(ValueError):
            node = LeafNode('a', None, None, None)

    def test_leaf_to_html(self):
        node = LeafNode('p', "This is a leaf", None, None)
        self.assertEqual(node.to_html(), "<p>This is a leaf</p>")

    
    def test_leaf_to_raw_text(self):
        node = LeafNode(None, "This is a leaf", None, None)
        self.assertEqual(node.to_html(), "This is a leaf")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")
