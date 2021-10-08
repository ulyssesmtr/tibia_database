from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:ulysses123@localhost/tibia_wiki_db'


CORS(app)
db = SQLAlchemy(app)


class Creature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    life = db.Column(db.Integer)
    exp = db.Column(db.Integer)

    def to_json(self):
        return {"id": self.id, "name": self.name, "life": self.life, "exp": self.exp}


@app.route('/')
def home():
    return 'Tibia wiki'


# Route to create a creature and store in the database
@app.route('/create_creature', methods=["POST"])
def create_creature():
    body = request.get_json()
    creature = Creature(name=body["name"].title(), life=body["life"], exp=body["exp"])
    all_creature_names = db.session.query(Creature.name).all()  # Get all the creature names from the db
    all_creature_names = [n[0].lower() for n in all_creature_names]  # Modify the data to a list of names
    if creature.name.lower() not in all_creature_names:
        db.session.add(creature)
        db.session.commit()

        return creature.to_json()
    else:
        return Response(status=409)


# Route to show the information of a specific creature, identified by its id
@app.route('/creature/<id>', methods=['GET'])
def show_creature(id):
    creature_object = Creature.query.filter_by(id=id).first()
    creature_json = creature_object.to_json()

    return json.dumps(creature_json)


# Route to show all the creatures
@app.route('/creatures', methods=['GET'])
def show_all_creatures():
    all_creatures_object_list = Creature.query.all()
    all_creatures_json_list = [creature.to_json() for creature in all_creatures_object_list]

    return json.dumps(all_creatures_json_list)


# Route to edit a specific creature,
@app.route('/creature/<id>', methods=['PUT'])
def search_creature(id):
    body = request.get_json()
    creature_object = Creature.query.filter_by(id=id).first()

    creature_object.name = body["name"]
    creature_object.life = body["life"]
    creature_object.exp = body["exp"]
    db.session.add(creature_object)
    db.session.commit()

    return creature_object.to_json()


# Route to delete a specific creature
@app.route('/creature/<id>', methods=['DELETE'])
def delete_creature(id):
    creature_object = Creature.query.filter_by(id=id).first()
    db.session.delete(creature_object)
    db.session.commit()

    return creature_object.to_json()

