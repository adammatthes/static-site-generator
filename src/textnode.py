from enum import Enum

class TextType(Enum):
    PLAIN = 'plaintext'
    BOLD = 'bold text'
    ITALIC = 'italic text'
    CODE = 'code text'
    LINK = 'link text'
    IMAGE = 'image/alt text'

class TextNode():
    def __init__(self, text, text_type, url):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, r_val):
        return self.text == r_val.text and \
                self.text_type == r_val.text_type and \
                self.url == r_val.url

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'
