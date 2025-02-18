from htmlnode import HTMLNode, ParentNode, LeafNode
from text import text_to_textnodes
from textnode import text_node_to_html_node, TextNode
import re

class MarkdownConst:
    PARAGRAPH = "paragraph"
    QUOTE = "quote"
    CODE = "code"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    HEADINGS = ["h1", "h2", "h3", "h4", "h5", "h6"]
    
class Tags:
    P = "p"
    BLOCKQUOTE = "blockquote"
    PRE = "pre"
    OL = "ol"
    UL = "ul"
    CODE = "code"
    LI = "li"
    

def markdown_to_html_node(markdown):
    parent = ParentNode(tag="div", children=[])
    
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        tag = block_type_to_html_tag(block_type)
        child_node = block_to_html_node(block, tag)
        parent.children.append(child_node)
        
    return parent
        
        
def block_to_html_node(block, tag):
    if tag == Tags.P:
        text = block.replace("\n", " ")
        return ParentNode(tag= Tags.P, children=text_to_children(text))
    
    elif tag in MarkdownConst.HEADINGS:
        text = block.lstrip("#").lstrip()
        return ParentNode(tag= tag, children=text_to_children(text))
    
    elif tag == Tags.BLOCKQUOTE:
        text = " ".join(line.lstrip("> ").strip() for line in block.split("\n"))
        return ParentNode(tag= Tags.BLOCKQUOTE, children=text_to_children(text))
    
    elif tag == Tags.PRE:
        text = "\n".join(block.split("\n")[1:-1])
        code_node = LeafNode(tag=Tags.CODE, value=text)
        return ParentNode(tag= Tags.PRE, children=[code_node]) 
    
    elif tag == Tags.UL:
        items = [line.lstrip("- ").lstrip("* ") for line in block.split("\n")]
        li_nodes = [ParentNode(tag=Tags.LI, children=text_to_children(item)) for item in items]
        return ParentNode(tag =Tags.UL, children=li_nodes)
    
    elif tag == Tags.OL:
        items = [line.split(". ", 1)[1] for line in block.split("\n")]
        li_nodes = [ParentNode(tag=Tags.LI, children=text_to_children(item)) for item in items]
        return ParentNode(tag =Tags.OL, children=li_nodes)
    
    raise ValueError("invalid block type")
        
    
    
    
    
def text_to_children(text):
    return list(map(text_node_to_html_node, (text_to_textnodes(text))))
    
        
def markdown_to_blocks(markdown):
    split_string = [block.strip() for block in markdown.split("\n\n") if block.strip()]
    return split_string

def block_to_block_type(block):
    lines = block.split("\n")
    
    if block.startswith('#'):
        count = 0
        for char in block:
            if char == "#":
                count += 1
                if count == 7:
                    return MarkdownConst.PARAGRAPH
            else:
                break
        return f"h{count}"
    if len(lines) > 1 and lines[0].startswith('```') and lines[-1].startswith('```'):
        return MarkdownConst.CODE
    if block.startswith('> '):
        for line in lines:
            if not line.startswith("> "):
                return MarkdownConst.PARAGRAPH
        return MarkdownConst.QUOTE
    if block.startswith('- ') or block.startswith('* '):
        for line in lines:
            if not line.startswith(('- ','* ')):
                return MarkdownConst.PARAGRAPH
        return MarkdownConst.UNORDERED_LIST
    if block.startswith('1. '):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return MarkdownConst.PARAGRAPH
            i += 1
        return MarkdownConst.ORDERED_LIST
    return MarkdownConst.PARAGRAPH

def block_type_to_html_tag(block_type):
    if block_type == MarkdownConst.PARAGRAPH:
        return Tags.P
    if block_type == MarkdownConst.QUOTE:
        return Tags.BLOCKQUOTE
    if block_type == MarkdownConst.CODE:
        return Tags.PRE
    if block_type == MarkdownConst.UNORDERED_LIST:
        return Tags.UL
    if block_type == MarkdownConst.ORDERED_LIST:
        return Tags.OL
    if block_type.startswith("h") and block_type[1] in '123456':
        return block_type
    return Tags.P
        
