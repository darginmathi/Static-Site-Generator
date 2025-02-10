from enum import Enum

class TextType(Enum):
    NORMAL_TEXT = "text"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINKS = "links"
    IMAGES = "images"
    
class TextNode:
    def __init__(self, text, text_type, url):
        self.text = text
        self.text_type = text_type 
        self.url = url
    
    def __eq__(self, other):
        return isinstance(self, other)

    def __repr__(self):
        return f"TextNode({self.text!r}, {self.text_type!r}, {self.url!r})"
    