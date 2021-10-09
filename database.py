from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from flask import Response

db = SQLAlchemy(None)


def setup(app):
    global db
    db = SQLAlchemy(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:ulysses123@localhost/tibia_wiki_db'


class Creature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    life = db.Column(db.Integer)
    exp = db.Column(db.Integer)

    def to_json(self):
        return {"id": self.id, "name": self.name, "life": self.life, "exp": self.exp}


def creating_creature(body):
    creature = Creature(name=body["name"].title(), life=body["life"], exp=body["exp"])
    all_creature_names = db.session.query(Creature.name).all()  # Get all the creature names from the db
    all_creature_names = [n[0].lower() for n in all_creature_names]  # Modify the data to a list of names
    if creature.name.lower() not in all_creature_names:
        db.session.add(creature)
        db.session.commit()
        return creature.to_json()
    else:
        return Response(status=409)


def showing_creature(id):
    creature_object = Creature.query.filter_by(id=id).first()

    return creature_object.to_json()


def showing_all_creatures():
    all_creatures_object_list = Creature.query.all()
    all_creatures_json_list = [creature.to_json() for creature in all_creatures_object_list]

    return all_creatures_json_list


def editing_creature(id, body):
    creature_object = Creature.query.filter_by(id=id).first()
    creature_object.name = body["name"]
    creature_object.life = body["life"]
    creature_object.exp = body["exp"]
    current_db_sessions = inspect(creature_object).session
    current_db_sessions.add(creature_object)
    # db.session.add(creature_object)
    # db.session.commit()
    current_db_sessions.commit()
    return creature_object.to_json()


def deleting_creature(id):
    creature_object = Creature.query.filter_by(id=id).first()
    current_db_sessions = inspect(creature_object).session
    current_db_sessions.delete(creature_object)
    current_db_sessions.commit()

    return creature_object.to_json()
