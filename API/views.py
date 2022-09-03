from flask import Blueprint, render_template, request
import json
import RealmEyeAPI.api as realmdata

views = Blueprint(__name__, 'views')

isSubmited = False

@views.route('/')
def index():
    return render_template('index.html', ign='')
@views.route("/", methods=['POST'])
def home():
    player = request.form['ign']
    data = realmdata.ReturnRealmEyeData(realmdata.getRealmEyeData(player), realmdata.getCharacters(player))
    button = True
    return render_template('index.html', button=True, ign=json.dumps(data, indent=3))
@views.route("/data")
def rawContent():
    args = request.args
    name = args.get('player')
    data = realmdata.ReturnRealmEyeData(realmdata.getRealmEyeData(name), realmdata.getCharacters(name))
    return render_template('raw.html', ign=json.dumps(data, indent=4))