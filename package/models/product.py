from package import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    production_emmission = db.Column(db.Integer)
    power_rating = db.Column(db.Float)
    power_duration = db.Column(db.Integer)
