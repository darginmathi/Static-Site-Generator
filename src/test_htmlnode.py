import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode


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
    
    

if __name__ == "__main__":
    unittest.main()
    