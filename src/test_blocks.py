import unittest
from pprint import pprint

from blocks import markdown_to_blocks, block_to_block_type, markdown_to_html_node
from text import TextNode
from htmlnode import HTMLNode, LeafNode

class TestSplitBlocks(unittest.TestCase):
    def test_example_case(self):
        string = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        expected = [
    '# This is a heading',
    'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
    '* This is the first list item in a list block\n* This is a list item\n* This is another list item'
    ]
        self.assertEqual(markdown_to_blocks(string), expected)
        
        
class TestMarkdownParser(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), "h1")
        self.assertEqual(block_to_block_type("###### Heading"), "h6")
        self.assertEqual(block_to_block_type("####### Heading"), "paragraph")  # Too many #'s
        
    def test_code(self):
        self.assertEqual(block_to_block_type("```\ncode here\n```"), "code")
        
    def test_quote(self):
        self.assertEqual(block_to_block_type("> quote"), "quote")
        self.assertEqual(block_to_block_type("> line 1\n> line 2"), "quote")
        
    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First\n2. Second\n3. Third"), "ordered_list")
        self.assertEqual(block_to_block_type("1. First\n3. Third"), "paragraph")  # Non-sequential
        self.assertEqual(block_to_block_type("2. Second"), "paragraph")  # Doesn't start with 1
        
        

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraph(self):
        markdown = """# Main Title

This is a paragraph with some *italic* and **bold** text.

> This is a quote

* List item 1
* List item 2

1. First ordered item
2. Second ordered item

```
code block here
```"""
        node = markdown_to_html_node(markdown)
        print_tree(node)
        
    def print_tree(node, level=0):
        indent = "  " * level
        tag = node.tag or "text"
        value = f'"{node.value}"' if node.value else ""
        print(f"{indent}{tag}: {value}")
        for child in node.children:
            print_tree(child, level + 1)
        
        
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )
        
if __name__ == "__main__":
    unittest.main()
