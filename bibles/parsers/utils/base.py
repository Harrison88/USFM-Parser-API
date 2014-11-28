import os
import glob
import logging as log
from collections import OrderedDict

class BaseParser(object):
    
    ext = None
    book_names = {"gen", "exo", "lev", "num", "deu", "jos", "jdg", "rut",
        "1sa", "2sa", "1ki", "2ki", "1ch", "2ch", "ezr", "neh", "est", "job",
        "psa", "pro", "ecc", "sng", "isa", "jer", "lam", "ezk", "dan", "hos",
        "jol", "amo", "oba", "jon", "mic", "nam", "hab", "zep", "hag", "zec",
        "mal", "mat", "mrk", "luk", "jhn", "act", "rom", "1co", "2co", "gal",
        "eph", "php", "col", "1th", "2th", "tit", "phm", "heb", "jas", "1pe",
        "2pe", "1jn", "2jn", "3jn", "jud", "rev"}
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.raw_data = ""
        self.data = OrderedDict()
        
        self.book = 0
        self.chapter = 0
        self.verse = 0
    
    def feed(self, data):
        self.raw_data += data
        self._parse()

    def _parse(self):
        self.raw_data = ""
    
    def add_text(self, text, book=0, chapter=0, verse=0):
        if book == 0:
            book = self.book
        if chapter == 0:
            chapter = self.chapter
        if verse == 0:
            verse = self.verse
        
        self.data[book][chapter][verse] = text

    def glob_ext(self, dir, ext=None):
        used_ext = self.ext
        if ext:
            used_ext = ext
        
        pattern = os.path.join(dir, "*.{0}".format(used_ext))
        return glob.glob(pattern)
