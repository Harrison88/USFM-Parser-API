import os
import flask
import bible as b

bible = b.BibleWrapper()
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route("/<id>")
def get(id):
    version = flask.request.args.get("version", "kjv")
    book, chapter, verse = int(id[0:2]), int(id[2:5]), int(id[5:8])
    try:
        if verse:
            return flask.jsonify({verse: bible.get(book, chapter, verse, version)})
        return flask.jsonify(bible.get(book, chapter, verse, version))
    except b.NonExistant:
        flask.abort(404)

@app.route("/list/")
def list_books():
    version = flask.request.args.get("version", "kjv")
    try:
        return flask.jsonify({"books": bible.list_books(version)})
    except b.NonExistant:
        flask.abort(404)
@app.route("/list/<book>")
def list_chapters(book):
    version = flask.request.args.get("version", "kjv")
    try:
        return flask.jsonify({book: bible.list_chapters(book, version)})
    except b.NonExistant:
        flask.abort(404)

@app.route("/list/<book>/<int:chapter>")
def list_verses(book, chapter):
    version = flask.request.args.get("version", "kjv")
    try:
        return flask.jsonify(bible.list_verses(book, chapter, version))
    except b.NonExistant:
        flask.abort(404)
