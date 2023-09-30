from flask import Flask, request
from flask_restful import Resource, Api
from secure_check import authenticate, identity
from flask_jwt import JWT, jwt_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
api = Api(app)

jwt = JWT(app, authenticate, identity)

# cars = [{'name': 'Volkswagen'}, {'name': 'Audi'}, .....]
cars = []

class Car(Resource):
    def get(self, name):
        for car in cars:
            if car['name'] == name:
                return car
        return {'name': None}, 404
    
    def post(self, name):
        new_car = {'name': name}
        cars.append(new_car)
        return new_car

    def delete(self, name):
        for car in cars:
            if car['name'] == name:
                cars.remove(car)
                return {'note': 'success'}
        return {'note': 'does not exist'}
    
class AllCars(Resource):

    @jwt_required()
    def get(self):
        return {'cars': cars}

api.add_resource(Car, '/car/<string:name>')
api.add_resource(AllCars, '/cars')

if __name__ == '__main__':
    app.run(debug=True)