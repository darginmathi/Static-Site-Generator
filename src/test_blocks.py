import unittest

from blocks import markdown_to_blocks, block_to_block_type

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
        self.assertEqual(block_to_block_type("# Heading"), "heading")
        self.assertEqual(block_to_block_type("###### Heading"), "heading")
        self.assertEqual(block_to_block_type("####### Heading"), "paragraph")  # Too many #'s
        
    def test_code(self):
        self.assertEqual(block_to_block_type("```\ncode here\n```"), "code")
        self.assertEqual(block_to_block_type("```code```"), "code")
        
    def test_quote(self):
        self.assertEqual(block_to_block_type("> quote"), "quote")
        self.assertEqual(block_to_block_type("> line 1\n> line 2"), "quote")
        
    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First\n2. Second\n3. Third"), "ordered_list")
        self.assertEqual(block_to_block_type("1. First\n3. Third"), "paragraph")  # Non-sequential
        self.assertEqual(block_to_block_type("2. Second"), "paragraph")  # Doesn't start with 1
        
        
        
if __name__ == "__main__":
    unittest.main()
