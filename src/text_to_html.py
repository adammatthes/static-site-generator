from textnode import TextNode, TextType
from htmlnode import LeafNode


def text_node_to_html(text_node):
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(None, text_node.text, None, None)
        case TextType.BOLD:
            return LeafNode('b', text_node.text, None, None)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text, None, None)
        case TextType.CODE:
            return LeafNode('code', text_node.text, None, None)
        case TextType.LINK:
            return LeafNode('a', text_node.text, None, {'href': text_node.url})
        case TextType.IMAGE:
            return LeafNode('img', '', None, {'src': text_node.url, 'alt': text_node.text})

