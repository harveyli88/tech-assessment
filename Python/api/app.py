# api/app.py

from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, request
# from flask_sqlalchemy import SQLAlchemy

# create an instantiation of the Flask app
app = Flask(__name__)
api = Api(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# db = SQLAlchemy(app)

# class OrderModel(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
# db.create_all()

# set environment config here
# app.config.from_object('project.config.DevelopmentConfig')

# TODO remove in-memory DB and use real one
orders = []

class Health(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'You keep using that word. I do not think it means what you think it means.'
        }

class Order(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'customerId',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'name',
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
    'orderId',
    type=int,
    required=True,
    help="This field cannot be left blank!"
    )
    # change to query
    def get(self, orderId):
        item = next(filter(lambda x: x['orderId'] == orderId, orders), None)
        return {'item': item}, 200 if item else 404    

    def post(self, orderId):
        if next(filter(lambda x: x['orderId'] == orderId, orders), None):
            return {'message': f'An order with orderId {orderId} already exists'}, 400

        data = Order.parser.parse_args()
        order = {'name': data['name'], 'price': data['price'],'customerId': data['customerId'],'orderId': orderId}
        orders.append(order)
        return order, 201

    def delete(self, orderId):
        global orders
        orders = list(filter(lambda x: x['orderId']!= orderId, orders))
        return {'message': "order Deleted"}, 200

    def put(self, orderId):
        data = Order.parser.parse_args()
        order = next(filter(lambda x: x['orderId']==orderId, orders), None)
        if order is None:
            order = {'name': data['name'], 'price': data['price'], 'customerId': data['customerId'], 'orderId': orderId}
            orders.append(order)
        else:
            order.update(data)
        return order

class Customer(Resource):
    def get(self, customerId):
        if customerId:
            result = []
            for order in orders:
                if order['customerId'] == customerId:
                    result.append(order)
            return result
        else:
            return "customerId not found", 500


class OrderList(Resource):
    def get(self):
        return {'orders':orders}

api.add_resource(Health, '/health')
api.add_resource(Order, '/order/<int:orderId>')
api.add_resource(Customer,'/customer/<int:customerId>')
api.add_resource(OrderList, '/orders')

if __name__ == '__main__':
    app.run(port=5000, debug=True)