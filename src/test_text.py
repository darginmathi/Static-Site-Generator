import unittest

from text import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType

class TestText(unittest.TestCase):
    def test_codeblock(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
        ])
        
    def test_invalid_delimiter(self):
        with self.assertRaises(Exception):
            split_nodes_delimiter([TextNode("Sample text", TextType.TEXT)], None, TextType.CODE)

    def test_no_delimiter_in_text(self):
        node = TextNode("This is plain text with no code", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [node]
        self.assertEqual(result, expected)

    def test_empty_text_node(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [node]  # Empty node remains unchanged
        self.assertEqual(result, expected)

    def test_empty_delimiter(self):
        node = TextNode("This is text", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "", TextType.CODE)
            
class TestExtract(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )
        
        
if __name__ == "__main__":
    unittest.main()