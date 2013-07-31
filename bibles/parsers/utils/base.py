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
        
        if verse in self.data[book][chapter]:
            current_text = self.data[book][chapter][verse]["text"]
            new_text = current_text + " " + text
            self.data[book][chapter][verse]["text"] = new_text
        else:
            self.data[book][chapter][verse] = {"text": text, "code": self.make_code(book, chapter, verse)}

    def glob_ext(self, dir, ext=None):
        used_ext = self.ext
        if ext:
            used_ext = ext
        
        pattern = os.path.join(dir, "*.{0}".format(used_ext))
        return glob.glob(pattern)
    
    def make_code(self, book, chapter=0, verse=0):
        def check(value, min, max):
            if value < min or value > max:
                raise ValueError("Illegal value ({0}) found during code creation".format(value))
        
        check(book, 1, 99)
        check(chapter, 0, 999)
        check(verse, 0, 999)
        
        if book < 10:
            book = "0" + str(book)
        else:
            book = str(book)
        
        if chapter < 10:
            chapter = "00" + str(chapter)
        elif chapter < 100:
            chapter = "0" + str(chapter)
        else:
            chapter = str(chapter)
        
        if verse < 10:
            verse = "00" + str(verse)
        elif verse < 100:
            verse = "0" + str(verse)
        else:
            verse = str(verse)
        
        return book + chapter + verse
