from flask import Flask, render_template, request, make_response
import api as realmdata
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', ign='')
@app.route("/", methods=['POST'])
def home():
    player = request.form['ign']
    data = realmdata.ReturnRealmEyeData(player)
    print(request.form.get('a'))
    test = ['Convert to JSON:', player]
    return render_template('index.html', ign=json.dumps(data, indent=3), test=test)
@app.route("/data")
def rawContent():
    args = request.args
    name = args.get('player')
    data = realmdata.ReturnRealmEyeData(name)
    resp = make_response(json.dumps(data, indent=4))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.content_type = 'application/json'
    return resp

