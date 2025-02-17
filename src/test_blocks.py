import unittest

from blocks import markdown_to_blocks

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
        
if __name__ == "__main__":
    unittest.main()
