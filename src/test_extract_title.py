import unittest
from generatepage import extract_title  # Replace `your_module` with the actual module name

class TestExtractTitle(unittest.TestCase):

    def test_extract_first_level1_heading(self):
        markdown = "# First Title\n\nSome text.\n\n# Second Title"
        self.assertEqual(extract_title(markdown), "First Title")
    
    def test_no_heading_raises_exception(self):
        markdown = "Some introductory text.\n\nNo headings here."
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "no heading found")
    
    def test_extract_heading_with_extra_spaces(self):
        markdown = "#   Title With Extra Spaces   "
        self.assertEqual(extract_title(markdown), "Title With Extra Spaces")
    
    def test_extract_heading_with_special_characters(self):
        markdown = "# !@#$%^&*()_+|~=`{}[]:\";'<>?,./"
        self.assertEqual(extract_title(markdown), "!@#$%^&*()_+|~=`{}[]:\";'<>?,./")
    
    def test_extract_heading_from_multiline_markdown(self):
        markdown = """
        This is some text.

        # A Valid Title

        More text here.
        """
        self.assertEqual(extract_title(markdown), "A Valid Title")
    
    def test_only_lower_level_headings(self):
        markdown = "## Subtitle\n### Another Subtitle\nSome text."
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "no heading found")
    
    def test_empty_markdown(self):
        markdown = ""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "no heading found")
    
    def test_whitespace_markdown(self):
        markdown = "     "
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "no heading found")


if __name__ == "__main__":
    unittest.main()
