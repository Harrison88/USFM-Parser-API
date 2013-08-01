import sys
import unittest

sys.path.append("..")

from bibles.parsers.utils import base
from bibles.parsers import usfm

class TestBaseParser(unittest.TestCase):
    
    def setUp(self):
        self.parser = base.BaseParser()
    
    def test_make_codes(self):
        self.assertEqual(self.parser.make_code(1), "01000000", "Book code was made incorrectly")
        self.assertEqual(self.parser.make_code(1, 1), "01001000", "Chapter code was made incorrectly")
        self.assertEqual(self.parser.make_code(1, 1, 1), "01001001", "Verse code was made incorrectly")
        
    def test_code_limits(self):
        make_code = self.parser.make_code
        self.assertRaises(ValueError, make_code, 100)
        self.assertRaises(ValueError, make_code, 1, 1000)
        self.assertRaises(ValueError, make_code, 1, 1, 1000)
        
        self.assertRaises(ValueError, make_code, -1)
        self.assertRaises(ValueError, make_code, 1, -1)
        self.assertRaises(ValueError, make_code, 1, 1, -1)
        
        self.assertRaises(ValueError, make_code, "foo")


usfm_beginning = """\\id MAT 40-MAT-kjv.sfm The King James Version of the Holy Bible Wednesday, October 14, 2009
\\ide UTF-8
\\h Matthew
\\toc1 The Gospel According to St. Matthew
\\toc2 Matthew
\\toc3 Mat
\\mt The Gospel According to St. Matthew"""

usfm_simple_verse = """\\c 1
\\v 1 The book of the generation of Jesus Christ, the son of David, the son of Abraham."""

usfm_nested_tags = """\\c 3
\\v 15 And Jesus answering said unto him, \\wj Suffer \\wj* \\add it to be so \\add* \\wj now: for thus it becometh us to fulfil all righteousness. \\wj* Then he suffered him."""

usfm_continued_text = """\\c 4
\\v 6 And saith unto him, If thou be the Son of God, cast thyself down: for it is written, He shall give his angels charge concerning thee: and in
\\add their \\add* hands they shall bear thee up, lest at any time thou dash thy foot against a stone."""

usfm_inconsistent_spacing = """\\c 4
\\v 25 And there followed him great multitudes of people from Galilee, and\\add from\\add* Decapolis, and \\wj\\add from\\add*\\wj* Jerusalem, and \\add from \\add* Judaea, and \\add from\\add* beyond Jordan."""

class TestUSFMParser(unittest.TestCase):
    
    def setUp(self):
        self.parser = usfm.USFMParser()
        self.parser.feed(usfm_beginning)
    
    def test_usfm_beginning(self):
        self.assertEqual(self.parser.data.keys(), [1])
    
    def test_usfm_simple_verse(self):
        self.parser.feed(usfm_simple_verse)
        
        self.assertEqual(self.parser.data[1][1][1]["text"],
            "The book of the generation of Jesus Christ, the son of David, the son of Abraham.")
        
    def test_usfm_nested_tags(self):
        self.parser.feed(usfm_nested_tags)
        
        self.assertEqual(self.parser.data[1][3][15]["text"],
            "And Jesus answering said unto him, Suffer it to be so now: for thus it becometh us to fulfil all righteousness. Then he suffered him.")
    
    def test_usfm_continued_text(self):
        self.parser.feed(usfm_continued_text)
        
        self.assertEqual(self.parser.data[1][4][6]["text"],
            "And saith unto him, If thou be the Son of God, cast thyself down: for it is written, He shall give his angels charge concerning thee: and in their hands they shall bear thee up, lest at any time thou dash thy foot against a stone.")

    def test_usfm_inconsistent_spacing(self):
        self.parser.feed(usfm_inconsistent_spacing)
        
        self.assertEqual(self.parser.data[1][4][25]["text"],
            "And there followed him great multitudes of people from Galilee, and from Decapolis, and from Jerusalem, and from Judaea, and from beyond Jordan.")
