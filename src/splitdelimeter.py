from textnode import TextNode, TextType
import re

def split_image_node(text):
    new_nodes = []

    segments = re.findall(r'\!\[.+\]\(.+\)|[^\!\[\]\(\)]+', text)

    for segment in segments:
        if segment.startswith('!'):
            alt_text = segment[2:segment.find(']')]
            url = segment[segment.find('(') + 1: segment.find(')')]
            new_node = TextNode(alt_text, TextType.IMAGE, url)
            new_nodes.append(new_node)
        else:
            new_node = TextNode(segment, TextType.PLAIN, '')
            new_nodes.append(new_node)

    return new_nodes


def split_link_node(text):
    new_nodes = []

    segments = re.findall(r'\[.+\]\(.+\)|[^\[\]\(\)]+', text)

    for segment in segments:
        if segment.startswith('['):
            link_text = segment[1:segment.find(']')]
            url = segment[segment.find('(') + 1: segment.find(')')]
            new_node = TextNode(link_text, TextType.LINK, url)
            new_nodes.append(new_node)
        else:
            new_node = TextNode(segment, TextType.PLAIN, '')
            new_nodes.append(new_node)

    return new_nodes



def split_nodes_delimeter(old_nodes, delimeter, text_type):
    new_nodes = []
    delimeters = {TextType.BOLD: "**",
                  TextType.ITALIC:  "_",
                  TextType.CODE: "`",
                  TextType.LINK: ("[", "]", "(", ")"),
                  TextType.IMAGE: ("!", "[", "]", "(", ")")}

    if text_type == TextType.IMAGE:
        for node in old_nodes:
            new_nodes.extend(split_image_node(node.text))
        return new_nodes

    if text_type == TextType.LINK:
        for node in old_nodes:
            new_nodes.extend(split_link_node(node.text))
        return new_nodes


    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        current_text = node.text.replace(delimeter, '@')
        segments = re.findall(f'@+.+@+|[^@]+', current_text)
        for segment in segments:
            if '@' in segment:
                new_node = TextNode(segment.strip('@'), text_type, '')
                new_nodes.append(new_node)
            else:
                new_node = TextNode(segment, TextType.PLAIN, '')
                new_nodes.append(new_node)

                        
    return new_nodes
