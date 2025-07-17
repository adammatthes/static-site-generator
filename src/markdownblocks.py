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


def markdown_to_html_alt(markdown):
    blocks = markdown_to_block(markdown)
    html = []

    for block in blocks:
        b_type = block_to_block_type(markdown)
        tokens = re.findall(r'[!\[].+\]\([^\)]+\)|[\*_`\>\-#]+|(?:\d\.)|[^#\*_`\>\[\]\n]+', block)
        tokens = list(filter(lambda x: not re.fullmatch(r'\s+', x), tokens))


        tag = b_type.value
        open_, close = f'<{tag}>', f'</{tag}>'
        length = len(tokens)
        i = 0

        print(tokens)
        while i < length:
            if tokens[i].startswith('!') and tokens[i].endswith(')'):
                open_, close = '<img>', '</img>'
                
                tokens.insert(i, open_)
                length += 1
                tokens.append(close)
                length += 1
                break

            if tokens[i].startswith('[') and tokens[i].endswith(')'):
                href_start = tokens[i].find('(') 
                href_end = tokens[i].find(')')
                text_start = tokens[i].find('[')
                text_end = tokens[i].find(']')
                open_, close = f'<a href="{tokens[i][href_start+1:href_end]}">', '</a>'
                tokens.insert(i, open_)
                length += 1
                
                if '[' in tokens[i][href_end:] and ')' in tokens[i][href_end:]:
                    tokens.insert(i+2, tokens[i][href_end + 1:])
                tokens[i+1] = tokens[i+1][text_start+1:text_end]
                
                if i + 2 > len(tokens):
                    tokens.append(close)
                else:
                    tokens.insert(i + 2, close)
                length += 1

                

            if '#' in tokens[i]:
                num = sum([t == "#" for t in tokens[i]])
                tokens[i] = f'<h{num}>'
                tokens.insert(i + 2, f'</h{num}>')
                length += 1
            if tokens[i] == '**':
                tokens[i] = '<b>'
                tokens[i+2] = '</b>'
            if tokens[i] == '_':
                tokens[i] = '<i>'
                tokens[i+2] = '</i>'


            if tokens[i] == '```':
                tokens[i] = '<pre><code>'
                end = i + 1
                while tokens[end] != '```':
                    end += 1
                tokens[end] = '</code></pre>'
                break
            elif tokens[i] == '`':
                tokens[i] = '<code>'
                tokens[i + 2] = '</code>'
            if tokens[i] == '>':
                number_of_lines = 1
                tokens[i] = '<blockquote>'
                bq = i + 2
                while bq < length and tokens[bq] == '>':
                    tokens[bq] = '<br>'
                    number_of_lines += 1
                    bq += 1
                tokens.insert(i + number_of_lines + 2, '</blockquote>')
                length += 1
            if tokens[i].strip() == '-':
                tokens.insert(i, '<ul>')
                length += 1
                item = i + 1
                while tokens.count('-'):
                    item = tokens.index('-')
                    tokens[item] = '<li>'
                    try:
                        close = tokens.index('-', item + 1)
                        tokens.insert(close, '</li>')
                    except:
                        tokens.append('</li>')
                    length += 1

                tokens.append("</ul>")
                length += 1
            if re.match(r'\d\.', tokens[i]):
                tokens.insert(i, '<ol>')
                length += 1
                item = i + 1
                while item < length and re.match(r'\d\.', tokens[item]):
                    tokens[item] = '<li>'
                    tokens.insert(item + 2, '</li>')
                    length += 1
                    item += 3
                tokens.insert(item, "</ol>")
                length += 1

            i += 1

        if b_type == BlockType.PARAGRAPH:
            pass
            #tokens.insert(0, "<p>")
            #tokens.append("</p>")
        html.append(''.join(tokens))

    return '\n'.join(html)


def extract_title(markdown):
    for line in markdown.split('\n'):
        if line.startswith('#'):
            return line.strip('#').strip()

    raise Exception('No h1 found in markdown')
