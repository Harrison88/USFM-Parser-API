import cPickle as pickle

class Bible(object):
    def __init__(self, version="asv"):
        try:
            self.bible = pickle.load(open("bibles/{}.pk1".format(version), "rb"))
        except IOError:
            raise NonExistant
        self.version = version
    
    def get_book(self, book):
        if book in self.bible:
            return self.bible[book]
        raise NonExistant("Book {} not in Bible".format(book))
    
    def get_chapter(self, book, chapter):
        book_dict = self.get_book(book)
        if chapter in book_dict:
            return book_dict[chapter]
        raise NonExistant("Book {} doesn't contain chapter {}".format(book, chapter))
    
    def get_verse(self, book, chapter, verse):
        chapter_dict = self.get_chapter(book, chapter)
        if verse in chapter_dict:
            return chapter_dict[verse]
        raise NonExistant("{} {} doesn't have a verse {}".format(book, chapter, verse))
    
    def get(self, book, chapter=0, verse=0):
        if verse > 0:
            return self.get_verse(book, chapter, verse)
        
        if chapter > 0:
            return self.get_chapter(book, chapter)
        
        return self.get_book(book)
    
    def list_books(self):
        return self.bible.keys()
    
    def list_chapters(self, book):
        book = self.get_book(book)
        return book.keys()
    
    def list_verses(self, book, chapter):
        chapter = self.get_chapter(book, chapter)
        return chapter.keys()

class BibleWrapper(object):
    def __init__(self):
        self.bibles = {}
    
    def load_version(self, version):
        if version not in self.bibles:
            self.bibles[version] = Bible(version)
    
    def get(self, book, chapter=0, verse=0, version="kjv"):
        if version not in self.bibles:
            self.load_version(version)
        return self.bibles[version].get(book, chapter, verse)
    
    def list_books(self, version="kjv"):
        self.load_version(version)
        return self.bibles[version].bible.keys()
    
    def list_chapters(self, book, version="kjv"):
        self.load_version(version)
        book = self.bibles[version].get_book(book)
        return book.keys()
    
    def list_verses(self, book, chapter, version="kjv"):
        self.load_version(version)
        chapter = self.bibles[version].get_chapter(book, chapter)
        return chapter.keys()

class NonExistant(Exception):
    pass
