import os
import flask
import bible as b

bible = b.BibleWrapper()
app = flask.Flask(__name__)
app.config["DEBUG"] = True

def generate_error(err, **kwargs):
    try:
        message = {"error": err.message}
        message.update(kwargs)
        return message
    except:
        flask.abort(500)

@app.route("/<id>")
def get(id):
    version = flask.request.args.get("version", "kjv")
    try:
        book, chapter, verse = int(id[0:2]), int(id[2:5]), int(id[5:8])
    except (IndexError, ValueError) as err:
        return flask.jsonify(generate_error(err, id=id, help="The ID you sent was malformed in some way; remember it should be in the form bbcccvvv like 01001001 for Genesis 1:1")), 400
        
    try:
        if verse:
            return flask.jsonify({verse: bible.get(book, chapter, verse, version)})
        return flask.jsonify(bible.get(book, chapter, verse, version))
    except b.NonExistant as err:
        return flask.jsonify(generate_error(err, id=id, version=version, help="That version or book/chapter/verse doesn't exist. If you're sure it does, that's a bug--please report it")), 404

@app.route("/list/")
def list_books():
    version = flask.request.args.get("version", "kjv")
    try:
        return flask.jsonify({"books": bible.list_books(version)})
    except b.NonExistant as err:
        return flask.jsonify(generate_error(err, version=version, help="That version doesn't appear to exist.")), 404
        
@app.route("/list/<book>")
def list_chapters(book):
    version = flask.request.args.get("version", "kjv")
    try:
        return flask.jsonify({book: bible.list_chapters(book, version)})
    except b.NonExistant as err:
        return flask.jsonify(generate_error(err, version=version, book=book, help="Either that version or that book doesn't exist. Make sure you're entering them correctly!")), 404

@app.route("/list/<book>/<int:chapter>")
def list_verses(book, chapter):
    version = flask.request.args.get("version", "kjv")
    try:
        return flask.jsonify(bible.list_verses(book, chapter, version))
    except b.NonExistant as err:
        return flask.jsonify(generate_error(err, version=version, book=book, chapter=chapter, help="Either that version, book, or chapter doesn't exist.")), 404

@app.route("/crash")
def crash():
    raise Exception("Test crash")

if app.config["DEBUG"] == True:
    from werkzeug.debug import DebuggedApplication
    app = DebuggedApplication(app, evalex=True)