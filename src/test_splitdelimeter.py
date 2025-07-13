import unittest
from textnode import TextNode, TextType
from splitdelimeter import split_nodes_delimeter, iterative_split

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
        node = TextNode("Check out ![my dog](https://www.cuteanimals.com)", TextType.PLAIN, '')
        new_nodes = split_nodes_delimeter([node], '!', TextType.IMAGE)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual([n.text_type for n in new_nodes], [TextType.PLAIN, TextType.IMAGE])

    def test_link_extract(self):
        node = TextNode("Follow my socials [here](https://www.link.tr)", TextType.PLAIN, '')
        new_nodes = split_nodes_delimeter([node], '[', TextType.LINK)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual([n.text_type for n in new_nodes], [TextType.PLAIN, TextType.LINK])

    def test_split_images(self):
        node = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.PLAIN, ''
                )
        new_nodes = split_nodes_delimeter([node], '!', TextType.IMAGE)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN, ''),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN, ''),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_two_links(self):
        text = "Here is a [link](https://www.example.com) and here is [another](https://www.google.com)"
        node = TextNode(text, TextType.PLAIN, '')
        new_nodes = split_nodes_delimeter([node], '[', TextType.LINK)
        print(new_nodes)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual([n.text_type for n in new_nodes], [TextType.PLAIN, TextType.LINK, TextType.PLAIN, TextType.LINK])

    def test_iterative_split(self):
        text = "Testing if _I_ can parse **all** text `types` with [one](https://www.functioncall.com) ![placeholder image](https://www.example.com)"
        node = TextNode(text, TextType.PLAIN, '')
        new_nodes = iterative_split([node])
        print(new_nodes)
        self.assertEqual(len(new_nodes), 10)
        self.assertEqual([n.text_type for n in new_nodes], [TextType.PLAIN, TextType.ITALIC, TextType.PLAIN, TextType.BOLD, TextType.PLAIN, TextType.CODE, TextType.PLAIN, TextType.LINK, TextType.PLAIN, TextType.IMAGE])
