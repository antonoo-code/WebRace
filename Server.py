from flask import Flask, request, send_from_directory
from flask_cors import CORS
import json
import secrets

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
    players[id]= {'status': None, 'name': name}
    print(players)
    return {'status': None, 'name': name,  'id': id}



@app.route("/game", methods=["PUT"])
def update_game():
    print(players)
    args = request.args
    id = args.get('id')
    if id not in players:
        return {'status':None}
    action = args.get('action')
    
    return {'status': None}

@app.route("/game", methods=["GET"])
def game_status():
    args = request.args
    id = args.get('id')
    return {'status': None}
    
if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)