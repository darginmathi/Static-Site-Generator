import unittest
from pprint import pprint

from text import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
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
        
class TestSplitImage(unittest.TestCase):
    def test_split_nodes_image_no_images(self):
        nodes = [TextNode("This is a text without images.", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(result, nodes)

    def test_split_nodes_image_single_image(self):
        nodes = [TextNode("This is an image: ![alt](image_url).", TextType.TEXT)]
        expected = [
            TextNode("This is an image: ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "image_url"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_image(nodes), expected)

    def test_split_nodes_image_multiple_images(self):
        nodes = [TextNode("Text before ![image1](url1) and ![image2](url2).", TextType.TEXT)]
        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("image1", TextType.IMAGE, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "url2"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_image(nodes), expected)

    def test_split_nodes_image_multiple_nodes(self):
        nodes = [
            TextNode("Node 1 with no image.", TextType.TEXT),
            TextNode("Node 2 with image: ![alt](image_url).", TextType.TEXT),
        ]
        expected = [
            TextNode("Node 1 with no image.", TextType.TEXT),
            TextNode("Node 2 with image: ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "image_url"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_image(nodes), expected)


class TestSplitLink(unittest.TestCase):
    def test_split_nodes_link_no_links(self):
        nodes = [TextNode("This is a text without links.", TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(result, nodes)

    def test_split_nodes_link_single_link(self):
        nodes = [TextNode("This is a link: [example](http://example.com).", TextType.TEXT)]
        expected = [
            TextNode("This is a link: ", TextType.TEXT),
            TextNode("example", TextType.LINK, "http://example.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_link(nodes), expected)

    def test_split_nodes_link_multiple_links(self):
        nodes = [TextNode("Text with [link1](http://link1.com) and [link2](http://link2.com).", TextType.TEXT)]
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "http://link1.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "http://link2.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_link(nodes), expected)

    def test_split_nodes_link_multiple_nodes(self):
        nodes = [
            TextNode("Node 1 with no link.", TextType.TEXT),
            TextNode("Node 2 with a link: [example](http://example.com).", TextType.TEXT),
        ]
        expected = [
            TextNode("Node 1 with no link.", TextType.TEXT),
            TextNode("Node 2 with a link: ", TextType.TEXT),
            TextNode("example", TextType.LINK, "http://example.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_link(nodes), expected)
        

class TestTestToNodes(unittest.TestCase):
    def test_one_line(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_multiple_links_and_images(self):
        text = "Here is [link1](http://example1.com), [link2](http://example2.com), and ![image1](http://example.com/image1.png)."
        result = text_to_textnodes(text)
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "http://example1.com"),
            TextNode(", ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "http://example2.com"),
            TextNode(", and ", TextType.TEXT),
            TextNode("image1", TextType.IMAGE, "http://example.com/image1.png"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected) 
        
    def test_mixed_markdown(self):
        text = "**Important:** Use the `code block` inside *italic* notes."
        expected = [
            TextNode("Important:", TextType.BOLD),
            TextNode(" Use the ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" inside ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" notes.", TextType.TEXT)
        ]
        self.assertEqual(text_to_textnodes(text), expected)    
        
        
if __name__ == "__main__":
    unittest.main()