import unittest
from markdownblocks import markdown_to_block, block_to_block_type, BlockType, markdown_to_html_node

class TestMarkdownBlock(unittest.TestCase):
        def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_block(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

        def test_block_to_block_type(self):
            text = '# this is a heading'
            self.assertEqual(block_to_block_type(text), BlockType.HEADING)
            self.assertEqual(block_to_block_type(text.replace(' ', '')), BlockType.PARAGRAPH)
            
            text = '```This is a code block```'
            self.assertEqual(block_to_block_type(text), BlockType.CODE)

            text = '>Start of a quote\n>and another quote line\n>and another quote line'
            self.assertEqual(block_to_block_type(text), BlockType.QUOTE)
            text = '>First line\nSecond line\n>third line'
            self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

            text = '- first item\n- second item\n- third item'
            self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)
            text = '- first item\n- second item\n-third item'
            self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

            text = '1. first item\n2. second item\n3. third item'
            self.assertEqual(block_to_block_type(text), BlockType.ORDERED_LIST)
            self.assertEqual(block_to_block_type(text.replace(' ', '')), BlockType.PARAGRAPH)

        def test_paragraphs(self):
            self.maxDiff = None
            md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

            node = markdown_to_html_node(md)
            html = node.to_html()
            print(html)
            self.assertEqual(
                html,
                "<div><p>This is </p><b>bolded</b><p> paragraph text in a p tag here</p><p>This is another paragraph with </p><i>italic</i><p> text and </p><code>code</code><p> here</p></div>",
            )

        def test_codeblock(self):
            self.maxDiff = None
            md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

            node = markdown_to_html_node(md)
            html = node.to_html()
            print(html)
            self.assertEqual(
                html,
                "<div><code>This is text that _should_ remain the **same** even with inline stuff</code></div>",
            )
