import os
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from secure_check import authenticate, identity
from flask_jwt import JWT, jwt_required

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

api = Api(app)
jwt = JWT(app, authenticate, identity)

################ Model ################

class Car(db.Model):

    __tablename__ = 'cars'
    name = db.Column(db.String(80),primary_key=True)

    def __init__(self, name):
        self.name=name

    def json(self):
        return {'name': self.name}
    
    def __str__(self):
        return f"{self.name}"


################ Resource ################
class CarResource(Resource):
    def get(self, name):

        car = Car.query.filter_by(name=name).first()
        if car:
            return car.json()
        else:
            return {'name': None}, 404
    
    def post(self, name):
        new_car = Car(name=name)
        db.session.add(new_car)
        db.session.commit()

        return new_car.json()

    def delete(self, name):
        car = Car.query.filter_by(name=name).first()
        db.session.delete(car)
        db.session.commit()

        return {'note': 'success'}
    
class AllCars(Resource):

    @jwt_required()
    def get(self):
        cars = Car.query.all()

        return [car.json() for car in cars]

api.add_resource(CarResource, '/car/<string:name>')
api.add_resource(AllCars, '/cars')

if __name__ == '__main__':
    app.run(debug=True)