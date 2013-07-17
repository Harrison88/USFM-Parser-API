import cPickle as pickle
import sys
if sys.version_info < (2, 7):
    # OrderedDict, the type that the Bibles are stored as, is new in 2.7.
    raise ImportError(("Python 2.7 or above is required;"
                       "you're using '{0}'").format(sys.version))

class Bible(object):

    """Bible is a helper for accessing a raw Bible.
    
    >>>b = Bible(version="kjv")
    """

    def __init__(self, version="asv"):
        """Initialize a Bible instance, loading a Bible from a file.
        
        Keyword argument:
        version -- a Bible version corresponding to a .pk1 file in bibles/ (default "asv")
        """
        try:
            self.bible = pickle.load(open("bibles/output/{}.pk1".format(version), "rb"))
        except IOError:
            raise NonExistant("version '{}' not found".format(version))
        self.version = version

    def get_book(self, book):
        """Get an entire book of the Bible.
        
        Argument:
        book -- A number 1-66 referring to a book in the Bible
        
        Returns an OrderedDict like {chapter1: {verse1: text, verse2: text2}}.
        """
        if book in self.bible:
            return self.bible[book]
        raise NonExistant("Book {} not in Bible".format(book))

    def get_chapter(self, book, chapter):
        """Get an entire chapter out of a book in the Bible.
        
        Arguments:
        book -- a number 1-66 referring to a book in the Bible
        chapter -- a chapter in the book
        
        Returns an OrderedDict like {verse1: text, verse2: text2}.
        """
        book_dict = self.get_book(book)
        if chapter in book_dict:
            return book_dict[chapter]
        raise NonExistant(("Book '{}' doesn't contain"
                           " chapter {}").format(book, chapter))

    def get_verse(self, book, chapter, verse):
        """Get the text of a specific verse.
        
        Arguments:
        book -- a number 1-66 referring to a book in the Bible
        chapter -- a chapter in the book
        verse -- a verse in the chapter
        
        Returns a regular dict like {"text": text, "code": code}
        where "code" is an eight digit id like 01001001 (Genesis 1:1).
        """
        chapter_dict = self.get_chapter(book, chapter)
        if verse in chapter_dict:
            return chapter_dict[verse]
        raise NonExistant(("Book '{}' chapter {} doesn't have"
                           " a verse {}").format(book, chapter, verse))

    def get(self, book, chapter=0, verse=0):
        """Get a book, chapter or verse using a get_* method.
        
        Required argument:
        book -- a number 1-66 referring to a book in the Bible
        
        Keyword arguments:
        chapter -- Get a chapter from the book, leave blank to get just a book
        verse -- Get a verse from the chapter, leave blank to get just a chapter
        
        Returns the result of the appropriate get_* method.
        """
        if verse > 0:
            return self.get_verse(book, chapter, verse)

        if chapter > 0:
            return self.get_chapter(book, chapter)

        return self.get_book(book)

    def list_books(self):
        """Returns a list of book keys."""
        return self.bible.keys()

    def list_chapters(self, book):
        """Returns a list of chapter numbers in a book."""
        book = self.get_book(book)
        return book.keys()

    def list_verses(self, book, chapter):
        """Returns a list of verse numbers in a chapter."""
        chapter = self.get_chapter(book, chapter)
        return chapter.keys()

class BibleWrapper(object):
    
    """BibleWrapper wraps multiple standard Bible objects into one.
    
    Supports nearly the same interface as Bible, with a keyword argument added:
    version -- the version of the Bible to use (default "kjv")
    
    Versions are implicitly loaded when an unloaded version is specified.
    """
    
    def __init__(self):
        """Initialize a BibleWrapper instance. No versions are loaded at this point."""
        self.bibles = {}

    def load_version(self, version):
        """Load a new version. Automatically called by other methods as needed, so don't worry about it too much.
        
        Maybe should be made private?"""
        if version not in self.bibles:
            self.bibles[version] = Bible(version)

    def get(self, book, chapter=0, verse=0, version="kjv"):
        """Calls Bible.get using the specified version. (default "kjv") """
        if version not in self.bibles:
            self.load_version(version)
        return self.bibles[version].get(book, chapter, verse)

    def list_books(self, version="kjv"):
        """Returns a list of book keys in the specified version. (default "kjv")"""
        self.load_version(version)
        return self.bibles[version].bible.keys()

    def list_chapters(self, book, version="kjv"):
        """Returns a list of chapter numbers in a book, using the specified version. (default "kjv")"""
        self.load_version(version)
        book = self.bibles[version].get_book(book)
        return book.keys()

    def list_verses(self, book, chapter, version="kjv"):
        """Returns a list of verse numbers in a chapter, using the specified version. (default "kjv")"""
        self.load_version(version)
        chapter = self.bibles[version].get_chapter(book, chapter)
        return chapter.keys()

class NonExistant(Exception):
    """The exception raised whenever something doesn't exist.
    
    This could be a book, chapter, verse, or even a version.
    They should probably be split out into subclasses for more exception-catching granularity.
    """
    pass
