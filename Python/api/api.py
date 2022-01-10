from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

CUSTOMERS = []
orders = {}

@app.route("/health")
def get():
        return {
            'status': 'success',
            'message': 'You keep using that word. I do not think it means what you think it means.'
        }

@app.route("/orders")
class Orders(Resource):
    def get(self, orderID):
        return {orderID: orders[orderID]}

    def put(self, orderID):
        orders[orderID] = request.form['data']
        return {orderID: orders[orderID]}










api.add_resource(Orders, '/<string:orderID>')

if __name__ == '__main__':
    app.run(debug=True)