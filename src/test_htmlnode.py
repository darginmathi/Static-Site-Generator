import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode



class TestHTMLNode(unittest.TestCase):
    def test_multiple(self):
        node = HTMLNode(props = {"class": "btn", "id": "submit-btn"})
        self.assertEqual(node.props_to_html(), 'class="btn" id="submit-btn"')
        
    def test_single(self):
        node = HTMLNode(props={"disabled": "True"})
        self.assertEqual(node.props_to_html(), 'disabled="True"')
    
    def test_empty(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")
        

class TestLeafNode(unittest.TestCase):        
    def test_tag_p(self):
        node = LeafNode(tag="p", value="Hello, World")
        self.assertEqual(node.to_html(), "<p>Hello, World</p>")
        
    def test_tag_a_with_props(self):
        node = LeafNode(tag="a", value="Click here", props={"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Click here</a>')
        
    def test_no_value(self):
        node = LeafNode(tag="p", value=None)
        with self.assertRaises(ValueError):
            node.to_html()
            
    def test_no_tag(self):
        node = LeafNode(tag=None, value="Just text")
        self.assertEqual(node.to_html(), "Just text")
    
    
class TestParentNode(unittest.TestCase):
    def test_tag_child(self):
        node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
)
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
        
    def test_tag_child_props(self):
        node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
    props={"href": "https://example.com"}
)
        self.assertEqual(node.to_html(), '<p href="https://example.com"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')
        
    def test_nested_parent_nodes(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "ul",
                    [
                        LeafNode("li", "Item 1"),
                        LeafNode("li", "Item 2"),
                    ],
                    props={"class": "list"}
                ),
                LeafNode("p", "Footer text"),
            ],
        )
        self.assertEqual(node.to_html(),'<div><ul class="list"><li>Item 1</li><li>Item 2</li></ul><p>Footer text</p></div>')
        
    def test_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("div", [])
            node.to_html()


if __name__ == "__main__":
    unittest.main()
    