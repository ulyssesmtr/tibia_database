from flask_sqlalchemy import SQLAlchemy


def setup(app):
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:ulysses123@localhost/tibia_wiki_db'


