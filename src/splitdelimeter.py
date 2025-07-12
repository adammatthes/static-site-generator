from textnode import TextNode, TextType

def split_nodes_delimeter(old_nodes, delimeter, text_type):
    new_nodes = []
    delimeters = {TextType.BOLD: "**",
                  TextType.ITALIC:  "_",
                  TextType.CODE: "`",
                  TextType.LINK: ("!", "[", "]", "(", ")"),
                  TextType.IMAGE: ("!", "[", "]", "(", ")")}

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        current_text = node.text
        current_delimeters = {}
        processed = set()
        i = 0
        while i < len(current_text):
            for d in delimeters.keys():
                delim_to_check = delimeters[d][0] if d in (TextType.LINK, TextType.IMAGE) else delimeters[d]
                if d not in current_delimeters:
                    current_delimeters[d] = []
                d_index = current_text.find(delim_to_check)
                if d_index != -1 and (d, d_index) not in processed:
                    current_delimeters[d].append(d_index)
                    processed.add((d, d_index))

            earliest_delimeter, e_index = None, float("inf")
            for k, v in current_delimeters.items():
                if len(v):
                    if v[0] < e_index:
                        earliest_delimeter = k
                        e_index = v[0]
            closing_index = -2

            if earliest_delimeter is None:
                #new_nodes.append(TextNode(current_text[i:], TextType.PLAIN, ''))
                return new_nodes

            if earliest_delimeter in (TextType.LINK, TextType.IMAGE):
                closing_index = current_text[e_index:].find(")")
            else:
                closing_index = current_text[e_index:].find(delimeters[earliest_delimeter][0])
            
            for k, v in current_delimeters.items():
                if k == earliest_delimeter:
                    continue
                if len(v) and v[0] < closing_index:
                    raise Exception("Invalid interlocking of tags")

            current_delimeters[earliest_delimeter].append(closing_index)
            
            processed.add((earliest_delimeter, closing_index))

            if earliest_delimeter in (TextType.LINK, TextType.IMAGE):
                l_bracket, r_bracket = current_text[e_index:].find('['), current_text[e_index:].rfind(']')
                l_paren, r_paren = current_text[e_index:].find('('), closing_index
                order = [l_bracket, r_bracket, l_paren, r_paren]
                if order != sorted(order):
                    raise Exception("Invalid link or image tag")

                new_node = TextNode(current_text[l_bracket+1:r_bracket],
                                    earliest_delimeter,
                                    current_text[l_paren+1:r_paren])

            else:
                before_non_text = current_text[:e_index]
                before_node = TextNode(before_non_text, TextType.PLAIN, '')
                new_nodes.append(before_node)
                
                new_node = TextNode(node.text[e_index + len(delimeters[earliest_delimeter]): closing_index],
                                    earliest_delimeter,
                                    '')
            
                new_nodes.append(new_node)

                after_non_text = current_text[closing_index:]
                after_node = TextNode(after_non_text, TextType.PLAIN, '')
                new_nodes.append(after_node)

            current_delimeters[earliest_delimeter].remove(e_index)
            current_delimeters[earliest_delimeter].remove(closing_index)
            i = closing_index

    return new_nodes
