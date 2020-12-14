from flask import Flask, render_template
from flask.globals import request
from flask.json import jsonify

from sparql.SparqlRepository import SparqlRepository

HOST = "localhost"
PORT = 5000

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def home():
    return "Hello World"


@app.route("/sparql", methods=["POST", "GET"])
def sparql():
    if request.method == "POST":
        query = request.form.get("query")
        sparql = SparqlRepository()
        return jsonify({"result": sparql.get_all_triples(query)})
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(use_reloader=True, debug=True)
