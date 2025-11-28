from flask import Flask, request, send_from_directory
from flask_cors import CORS
import json
import secrets
from game import Game


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
    status = {'status': None}
    if id not in players:
        return status
    action = args.get('action')
    if action == 'fly':
        pass
    elif action == 'dice':
        pass
    elif action == 'charge':
        pass
    elif action == 'supercharge':
        pass
    elif action == 'locationQuery':
        pass 
    
    return status

@app.route("/game", methods=["GET"])
def game_status():
    args = request.args
    id = args.get('id')
    game = players[id]['game']
    stats = game.get_statistics()
    return {'status': stats}
    
if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)