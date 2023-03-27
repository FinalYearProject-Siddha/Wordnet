from flask import Flask, render_template, request, redirect, url_for
import json
from json2html import *

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', show = False)

@app.route('/results', methods = ['GET', 'POST'])
def results():
    with open('static/relationship.json', encoding="utf8") as f:
        contents = f.read()
        rels = json.loads(contents)
    if request.method == "POST":
        data = request.form[list(request.form.keys())[0]]
        if list(request.form.keys())[0] == 'tam-inp' and all(chr.isalpha() or chr.isspace() for chr in data.strip()) and data != "":
            redirect(url_for("home"))
            return render_template('index.html', msg="Please enter Tamil text or select 'Type in English'!")
        if data == "":
            redirect(url_for("home"))
            return render_template('index.html', msg="Please enter valid text")
        if data.strip() not in rels.keys():
            return render_template('not_found.html', show = "Oh no! The requested resource isn't available!")
        table_html = json2html.convert(json = rels[data.strip()], table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\"")
        return render_template('results.html', show = table_html, term = data.strip())
    

if __name__ == '__main__':
    app.run(debug=True)