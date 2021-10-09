from flask import Flask, Response, request
import json
from flask_cors import CORS
import database

app = Flask(__name__)
database.setup(app)
CORS(app)


@app.route('/')
def home():
    return 'Tibia wiki'


# Route to create a creature and store in the database
@app.route('/create_creature', methods=["POST"])
def create_creature():
    body = request.get_json()
    creature_json = database.creating_creature(body)

    return creature_json


# Route to show the information of a specific creature, identified by its id
@app.route('/creature/<id>', methods=['GET'])
def show_creature(id):
    creature_json = database.showing_creature(id)

    return json.dumps(creature_json)


# Route to show all the creatures
@app.route('/creatures', methods=['GET'])
def show_all_creatures():
    all_creatures_json_list = database.showing_all_creatures()

    return json.dumps(all_creatures_json_list)


# Route to edit a specific creature,
@app.route('/creature/<id>', methods=['PUT'])
def edit_creature(id):
    body = request.get_json()
    creature_object_json = database.editing_creature(id, body)

    return creature_object_json


# Route to delete a specific creature
@app.route('/creature/<id>', methods=['DELETE'])
def delete_creature(id):
    creature_object_json = database.deleting_creature(id)

    return creature_object_json

