from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Pokemon(db.Model):
    __tablename__ = 'pokemon'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'), nullable=False)
    generation_id = db.Column(db.Integer, db.ForeignKey('generations.id'), nullable=False)
    habitat_id = db.Column(db.Integer, db.ForeignKey('habitats.id'), nullable=False)
    abilities_id = db.Column(db.Integer, db.ForeignKey('abilities.id'), nullable=False)
    moves_id = db.Column(db.Integer, db.ForeignKey('moves.id'), nullable=False)

class Types(db.Model):
    __tablename__ = 'types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class Generations(db.Model):
    __tablename__ = 'generations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class Habitats(db.Model):
    __tablename__ = 'habitats'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class Abilities(db.Model):
    __tablename__ = 'abilities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class Moves(db.Model):
    __tablename__ = 'moves'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)