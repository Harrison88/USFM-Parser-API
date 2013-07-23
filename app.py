import sys
import flask
from bibles import wrappers as b

bible = b.MultiBibleWrapper()
app = flask.Flask(__name__)
app.config["DEBUG"] = True

def generate_error(err, **kwargs):
    """Generate an error message to be sent to client.
    
    There really is no reason for the try/except block. Should be removed.
    """
    try:
        message = {"error": err.message}
        message.update(kwargs)
        return message
    except:
        flask.abort(500)

@app.route("/<id>")
def get(id):
    
    """Get a Bible ID and convert it to JSON.
    
    Argument:
    id -- an eight digit ID like 01001001 (Genesis 1:1)
        This is automatically filled in by Flask when a url like /01001001 is visited
    
    A specific version can be used by passing in a version argument in the query string. (default "kjv")
    """
    
    version = flask.request.args.get("version", "kjv")
    try:
        book, chapter, verse = int(id[0:2]), int(id[2:5]), int(id[5:8])
    except (IndexError, ValueError) as err:
        return flask.jsonify(generate_error(err, id=id,
                                help=("The ID you sent was malformed in some"
                                " way; remember it should be in the form"
                                " bbcccvvv like 01001001 for Genesis 1:1"))), 400

    try:
        return flask.jsonify(bible.get(book, chapter, verse, version))
    except b.NonExistant as err:
        return flask.jsonify(generate_error(err, id=id, version=version,
                                help=("That version or book/chapter/verse"
                                " doesn't exist. If you're sure it does,"
                                " that's a bug--please report it"))), 404

@app.route("/list/")
def list_books():
    """Get a list of book keys and convert it to JSON.
    
    The URL is "/list/".
    
    First puts the list in a dict like this {"books": list_of_book_keys} because Flask likes dicts at the top level of JSON output.
    http://flask.pocoo.org/docs/security/#json-security
    """
    version = flask.request.args.get("version", "kjv")
    try:
        return flask.jsonify({"books": bible.list_books(version)})
    except b.NonExistant as err:
        return flask.jsonify(generate_error(err, version=version,
                                help="That version doesn't appear to exist.")), 404

@app.route("/list/<int:book>")
def list_chapters(book):
    """Get a list of chapter numbers in a book and convert it to JSON.
    
    The URL is "/list/<book>".
    
    Argument:
    book -- the book key get the chapters of.
        Automatically filled in by Flask when a URL like "/list/1" is visited.
    
    A specific version can be used by passing in a "version" argument in the query string. (default "kjv")
    """
    version = flask.request.args.get("version", "kjv")
    try:
        return flask.jsonify({book: bible.list_chapters(book, version)})
    except b.NonExistant as err:
        return flask.jsonify(generate_error(err, version=version, book=book,
                                help=("Either that version or that book"
                                " doesn't exist. Make sure you're entering"
                                " them correctly!"))), 404

@app.route("/list/<book>/<int:chapter>")
def list_verses(book, chapter):
    """Get a list of verse numbers in a chapter and convert it to JSON.
    
    The URL is "/list/<book>/<int:chapter>".
    
    Arguments:
    book -- the book key.
    chapter -- the chapter number to get the verses of.
        These are automatically filled in by Flask when a URL like "/list/1/1" is visited.
    
    A specific version can be used by passing in a version argument in the query string. (default "kjv")
    """
    version = flask.request.args.get("version", "kjv")
    try:
        return flask.jsonify(bible.list_verses(book, chapter, version))
    except b.NonExistant as err:
        return flask.jsonify(generate_error(err, version=version, book=book,
                                chapter=chapter, help=("Either that version,"
                                    " book, or chapter doesn't exist."))), 404

@app.route("/crash")
def crash():
    """A test to see what happens when the app crashes. Use it to play around with the debugger."""
    raise Exception("Test crash")

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8080
    for arg in sys.argv:
        if "--host" in arg:
            host = arg.split("=")[1]
        elif "--port" in arg:
            port = int(arg.split("=")[1])

    app.run(host=host, port=port)
