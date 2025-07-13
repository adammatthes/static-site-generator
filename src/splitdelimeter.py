from textnode import TextNode, TextType
import re

def split_nodes_delimeter(old_nodes, delimeter, text_type):
    new_nodes = []
    delimeters = {TextType.BOLD: "**",
                  TextType.ITALIC:  "_",
                  TextType.CODE: "`",
                  TextType.LINK: ("[", "]", "(", ")"),
                  TextType.IMAGE: ("!", "[", "]", "(", ")")}


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
