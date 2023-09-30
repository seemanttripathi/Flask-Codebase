from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

cars = []

class Car(Resource):
    def get(self, name):
        for car in cars:
            if car['name'] == name:
                return car
        return {'name': None}
    
    def post(self, name):
        new_car = {'name': name}
        cars.append(new_car)
        return new_car

    def delete(self, name):
        for car in cars:
            if car['name'] == name:
                cars.remove(car)
                return {'note': 'success'}
        return {'note': 'did not exits'}
    
class AllCars(Resource):
    def get(self):
        return {'cars': cars}

api.add_resource(Car, '/car/<string:name>')
api.add_resource(AllCars, '/cars')

if __name__ == '__main__':
    app.run(debug=True)