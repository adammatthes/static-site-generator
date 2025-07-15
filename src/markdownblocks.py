from splitdelimeter import *
from textnode import TextNode, TextType
from enum import Enum
import re
from htmlnode import HTMLNode, LeafNode, ParentNode

class BlockType(Enum):
    PARAGRAPH = 'p'
    HEADING = 'h'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'ul'
    ORDERED_LIST = 'ol'


def is_heading(block):
    return re.fullmatch(r'#{1,6} .+', block)

def is_code(block):
    return block.startswith('```') and block.endswith('```')

def is_quote(block):
    for b in block.split('\n'):
        if not b.startswith('>'):
            return False

    return True

def is_unordered_list(block):
    for b in block.split('\n'):
        if not b.startswith('- '):
            return False

    return True

def is_ordered_list(block):
    for i, b in enumerate(block.split('\n')):
        if not b.startswith(f'{i+1}. '):
            return False

    return True

def block_to_block_type(block):
    match block:
        case b if is_heading(b):
            return BlockType.HEADING
        case b if is_code(b):
            return BlockType.CODE
        case b if is_quote(b):
            return BlockType.QUOTE
        case b if is_unordered_list(b):
            return BlockType.UNORDERED_LIST
        case b if is_ordered_list(b):
            return BlockType.ORDERED_LIST
        case _:
            return BlockType.PARAGRAPH
        



def markdown_to_block(markdown):
    blocks = markdown.split('\n\n')

    for i in range(len(blocks)):
        blocks[i] = blocks[i].strip()

    blocks = list(filter(lambda x: x != '', blocks))

    return blocks


def strip_markdown(markdown, block_type):
    match block_type:
        case BlockType.HEADING:
            return markdown.lstrip('#')
        case BlockType.CODE:
            return markdown.strip('`')
        case BlockType.QUOTE:
            lines = markdown.split('\n')
            for i in range(len(lines)):
                lines[i] = lines[i][2:]
            return '\n'.join(lines)
        case BlockType.UNORDERED_LIST:
            lines = markdown.split('\n')
            for i in range(len(lines)):
                lines[i] = lines[i][2:]
            return '\n'.join(lines)
        case BlockType.ORDERED_LIST:
            lines = markdown.split('\n')
            for i in range(len(lines)):
                lines[i] = lines[i][3:]
            return '\n'.join(lines)
        case _:
            return markdown




def markdown_to_html_node(markdown):
    blocks = markdown_to_block(markdown)

    children = []
    for block in blocks:
        b_type = block_to_block_type(block)
        content = re.sub(r'[^\S\n]{2,}', ' ', strip_markdown(block, b_type)).strip()
        if b_type != BlockType.CODE:
            text_nodes = iterative_split([TextNode(content.replace('\n', ''), TextType.PLAIN, '')])
        else:
            text_nodes = [TextNode(content.replace('\n', ''), TextType.CODE, '')]
        for n in text_nodes:
            leaf = LeafNode(n.text_type.value, n.text, None, None)
            children.append(leaf)
    
    parent = ParentNode('div', children, None)

    return parent
    
