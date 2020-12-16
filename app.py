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
        query = {}
        query['title'] = request.form.get("title")
        query['cast'] = request.form.get("cast")
        query['director'] = request.form.get("director")        
        query['writer'] = request.form.get("writer")        
        query['genre'] = request.form.get("genre")        
        query['rating'] = request.form.get("rating")        
        query['company'] = request.form.get("company")        

        sparql = SparqlRepository()
        return jsonify({"result": sparql.get_triples(query)})
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(use_reloader=True, debug=True)
