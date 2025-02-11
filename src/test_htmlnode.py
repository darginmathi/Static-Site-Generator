import unittest

from htmlnode import HTMLNode


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
    

if __name__ == "__main__":
    unittest.main()
    