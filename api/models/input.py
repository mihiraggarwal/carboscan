from api.main import db

class Input(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cookie = db.Column(db.Integer, nullable=False)
    type_device = db.Column(db.Boolean, nullable=False)
    device_country = db.Column(db.String)
    device_name = db.Column(db.Integer)
    device_quantity = db.Column(db.Integer)
    device_time = db.Column(db.Integer)
    flight_origin = db.Column(db.String)
    flight_destination = db.Column(db.String)
    flight_airline = db.Column(db.String)
    flight_number = db.Column(db.Integer)
    flight_date = db.Column(db.Date)
    flight_class = db.Column(db.String)