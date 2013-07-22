import os
import glob

class BaseParser(object):
    
    ext = None
    
    def __init__(self, file):
        self.file = file
    
    def glob_ext(self, dir, ext=None):
        used_ext = self.ext
        if ext:
            used_ext = ext
        
        pattern = os.path.join(dir, "*.{0}".format(used_ext))
        return glob.glob(pattern)
    
    def make_code(self, book, chapter=0, verse=0):
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
    
    def parse(self):
        pass
