from flask import Flask, render_template, request, redirect, url_for
from googletrans import Translator, constants
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
        json_data = rels[data.strip()]
        tamil_json_data = {}
        translator = Translator()
        for (k,v) in json_data.items():
            if k=='Category':
                translation = translator.translate(v, src="ta")
                tamil_json_data[k] = translation.text
            else:
                for value in json_data[k]:
                    translation = translator.translate(value, src="ta")
                    if k in tamil_json_data.keys():
                        tamil_json_data[k].append(translation.text)
                    else:
                        tamil_json_data[k] = [translation.text]
        table_html = json2html.convert(json = json_data, table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\"")
        tamil_table_html = json2html.convert(json = tamil_json_data, table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\"")
        return render_template('results.html', json = table_html, tamil_json = tamil_table_html, term = data.strip(), tamil_term = translator.translate(data.strip()).text)
    

if __name__ == '__main__':
    app.run(debug=True)