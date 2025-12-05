from flask import Flask, request, send_from_directory
from flask_cors import CORS
import json
import secrets
from game import Game, get_airport_name
from dotenv import load_dotenv
import os

load_dotenv()



players = {}

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def front_page():
    return send_from_directory("static", "index.html")

@app.route("/game", methods=["POST"])
def new_game():
    args = request.args
    name = args.get('name')
    id = secrets.token_hex(8)
    game = Game(0)
    stats = game.get_statistics()
    players[id]= {'name': name, 'game': game}
    return {'name': name,  'id': id, 'stats':stats}



@app.route("/game", methods=["PUT"])
def update_game():
    args = request.args
    id = args.get('id')
    status = {'stats': None}
    if id not in players:
        return status
    game = players[id]['game']
    action = args.get('action')
    if action == 'fly':
        icao = args.get('icao')
        status['stats']= game.do_fly(icao)
    elif action == 'dice':
        status['stats'] = game.throw_dice()
    elif action == 'charge':
        status['stats'] = game.charge()
    elif action == 'supercharge':
        pass
    elif action == 'locationQuery':
        status['stats']= game.get_statistics()
        npc_icao = game.npc_current_airport
        npc_airport = get_airport_name(npc_icao)
        status['npc_airport']= npc_airport
    
    return status

@app.route("/game", methods=["GET"])
def game_status():
    args = request.args
    id = args.get('id')
    game = players[id]['game']
    stats = game.get_statistics()
    return {'stats': stats}
if __name__ == '__main__':
    app.run(use_reloader=True, host=os.environ.get('FLASK_HOST'), port=os.environ.get('FLASK_PORT'))
    