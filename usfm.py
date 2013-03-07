import sys
import glob
import os
import cPickle
from collections import OrderedDict

def main():
    output = OrderedDict()
    
    directory = sys.argv[1]
    files = sorted(glob.glob(os.path.join(directory, "*.usfm")))
    for usfm_file in files:
        number = int(os.path.split(usfm_file)[-1][0:2]) #Magic!
        if number > 39 and number < 64: #Weed out apocrypha
            continue
        if number > 63:
            number -= 24 #Get rid of non-existant apocryphal book numbers
        content, book_name, short_name = parse_usfm(open(usfm_file).readlines())
        output[number] = content
        output[book_name] = content
        output[short_name] = content
    
    out_file = open(sys.argv[2], "w")
    cPickle.dump(output, out_file)

def parse_usfm(lines):
    collect_anyway = ["wj", "add", "nd", "pn", "qt", "sig", "tl", "em", "bd", "it", "bdit", "no", "sc"]
    out = OrderedDict()
    chapter = 0
    for line in lines:
        if line.startswith("\\v"):
            words = line.split()
            verse_number = int(words[1])
            verse_text = []
            collect = True
            for word in words[2:]:
                if "\\" in word and "*" not in word:
                    collect = False
                    for tag in collect_anyway:
                        if tag in word:
                            collect = True
                            break
                elif "\\" in word and "*" in word:
                    collect = True
                elif collect == True:
                    verse_text.append(word)
            out[chapter][verse_number] = " ".join(verse_text)
        elif line.startswith("\\q"):
            words = line.split()
            if len(words) == 1:
                continue
            verse = out[chapter][verse_number]
            verse += " " + " ".join(words[1:])
            out[chapter][verse_number] = verse
        elif line.startswith("\\c"):
            chapter = int(line.split()[1])
            out[chapter] = OrderedDict()
        elif line.startswith("\\toc2"):
            book_name = "".join(line.split()[1:])
        elif line.startswith("\\toc3"):
            short_name = line.split()[1]
    
    return out, book_name, short_name

if __name__ == "__main__":
    main()
