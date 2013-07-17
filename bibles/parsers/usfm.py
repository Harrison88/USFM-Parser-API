import sys
import os
import cPickle as pickle
from collections import OrderedDict

from utils.base import BaseParser
from utils.zip_tools import unzip

class USFMParser(BaseParser):
    
    ext = "usfm"
    
    def parse(self):
        unzipped = unzip(self.file)
        if not unzipped:
            return False
        
        output = OrderedDict()
        filenames = sorted(self.glob_ext(unzipped))
        for filename in filenames:
            number = int(os.path.split(filename)[-1][0:2])
            if number > 39 and number < 64:
                continue
            if number > 63:
                number -= 24
            
            code = self.make_code(number)
            
            with open(filename) as usfm_file:
                output[code] = self.parse_file(usfm_file, number)
            
        return pickle.dumps(output)
    
    def parse_file(self, usfm_file, book_number):
        output = OrderedDict()
        for line in usfm_file:
            if line.startswith("\\v"):
                tokens = line.split()
                verse = int(tokens[1])
                verse_code = self.make_code(book_number, chapter, verse)
                verse_text = self.collect_text(tokens[2:])
                
                output[chapter][verse] = {"text": verse_text, "code": verse_code}
            
            elif line.startswith("\\q"):
                tokens = line.split()
                if len(tokens) == 1:
                    continue
                
                text = output[chapter][verse]["text"]
                text += " " + " ".join(tokens[1:])
                output[chapter][verse]["text"] = text
            
            elif line.startswith("\\c"):
                chapter = int(line.split()[1])
                chapter_code = self.make_code(book_number, chapter)
                
                output[chapter] = OrderedDict({"code": chapter_code})
            
        return output
    
    def collect_text(self, tokens):
        collect_anyway = ["wj", "add", "nd", "pn", "qt", "sig", "tl", "em", "bd", "it", "bdit", "no", "sc"]
        text = []
        
        collect = True
        for token in tokens:
            if "\\" in token and "*" not in token:
                collect = False
                for tag in collect_anyway:
                    if tag in token:
                        collect = True
                        break
            
            elif "\\" in token and "*" in token:
                collect = True
            
            elif collect:
                text.append(token)
        
        return " ".join(text)