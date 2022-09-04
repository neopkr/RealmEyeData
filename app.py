from flask import Flask, render_template, request
import api as realmdata
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', ign='')
@app.route("/", methods=['POST'])
def home():
    player = request.form['ign']
    data = realmdata.ReturnRealmEyeData(realmdata.getRealmEyeData(player), realmdata.getCharacters(player))
    return render_template('index.html', button=True, ign=json.dumps(data, indent=3))
@app.route("/data")
def rawContent():
    args = request.args
    name = args.get('player')
    data = realmdata.ReturnRealmEyeData(realmdata.getRealmEyeData(name), realmdata.getCharacters(name))
    return render_template('raw.html', ign=json.dumps(data, indent=4))

