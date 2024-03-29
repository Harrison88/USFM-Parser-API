import sys
import os
import cPickle as pickle
from collections import OrderedDict

from utils.base import BaseParser
from utils.zip_tools import unzip

class USFMParser(BaseParser):
    
    ext = "usfm"
    continued_text_tags = {"\\wj", "\\add", "\\nd", "\\pn", "\\qt", "\\sig", "\\tl", "\\em", "\\bd", "\\it", "\\bdit", "\\no", "\\sc", "\\q"}
    
    def _parse(self):
        usfm_lines = self.raw_data.splitlines()
        self.raw_data = ""
        for line in usfm_lines:
            if self.parse_line(line) is False:
                break
    
    def parse_line(self, line):
        tokens = self.tokenize(line)
        tag = tokens[0]
        
        if tag == "\\v":
            verse_number = self.verse = int(tokens[1])
            self.add_text(self.collect_text(tokens[2:]))
        
        elif tag in self.continued_text_tags:
            if tag == "\\q":
                if len(tokens) == 1:
                    return
                self.add_text(self.collect_text(tokens[1:]))
            else:
                self.add_text(self.collect_text(tokens))
        
        elif tag == "\\c":
            chapter = self.chapter = int(tokens[1])
            self.data[self.book][chapter] = OrderedDict()
        
        elif tag == "\\toc3":
            if tokens[1].lower() not in self.book_names:
                return False
            self.book += 1
            self.data[self.book] = OrderedDict()
    
    def collect_text(self, tokens):
        text = []
        
        collect = True
        for token in tokens:
            if "\\" in token and "*" not in token:
                collect = False
                if token in self.continued_text_tags:
                    collect = True
            
            elif "\\" in token and "*" in token:
                collect = True
            
            elif collect:
                text.append(token)
        
        return " ".join(text)
    
    def tokenize(self, line):
        tokens = line.split()
        new = []
        for token in tokens:
            if "\\" in token and not token.startswith("\\"):
                split = token.split("\\")
                new.append(split[0])
                del split[0]
                for tag in split:
                    new.append("\\" + tag)
                
            elif "\\" in token and token.startswith("\\"):
                if len(token.split("\\")) > 2:
                    new.extend(["\\" + tag for tag in token.split("\\")])
                else:
                    new.append(token)
                
            else:
                new.append(token)
        
        return new
    
    def parse_zip(self, zip_file):
        unzipped = unzip(zip_file)
        if not unzipped:
            return False

        filenames = sorted(self.glob_ext(unzipped))
        for filename in filenames:
            with open(filename) as usfm_file:
                self.feed(usfm_file.read())
            
        return True
