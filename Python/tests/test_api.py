# api/tests/test_api.py

import json
import os

import unittest
import pytest
from flask import Flask
from flask_restful import Resource, Api, reqparse, request

from Python.api.app import app

class BaseCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()


class Test_Api(BaseCase):
    def test_health(self):
        resp = self.app.get('/health')
        data = json.loads(resp.data.decode())
        assert resp.status_code == 200
        assert 'You keep using that word. I do not think it means what you think it means.' in data['message']
        assert 'success' in data['status']

    def test_get_order_by_Id(self):
        order_payload_1 = {
            "name": "chair",
            "price": 15.99,
            "customerId": 1,
            "orderId": 1
        }
        order_payload_2 = {
            "name": "table",
            "price": 5.99,
            "customerId": 1,
            "orderId": 2
        }
        self.app.post('/order/1', headers={"Content-Type": "application/json"}, data=json.dumps(order_payload_1))
        self.app.post('/order/2', headers={"Content-Type": "application/json"}, data=json.dumps(order_payload_2))

        resp = self.app.get('/customer/1')
        data = json.loads(resp.data.decode())

        assert len(data) == 2
        

    def test_post(self):
        order_payload = {
            "name": "chair",
            "price": 15.99,
            "customerId": 3,
            "orderId": 5
        }
        resp = self.app.post('/order/5', headers={"Content-Type": "application/json"}, data=json.dumps(order_payload))
        self.assertEqual(201, resp.status_code)


    def test_delete(self):
        resp = self.app.delete('/order/2')
        data = json.loads(resp.data.decode())
        assert 'order Deleted' in data["message"]
        self.assertEqual(200, resp.status_code)

    def test_update(self):
        order_payload = {
            "name": "chair",
            "price": 1.99,
            "customerId": 1,
            "orderId": 2
        }
        resp = self.app.put('/order/2', headers={"Content-Type": "application/json"}, data=json.dumps(order_payload))
        data = json.loads(resp.data.decode())
        print(data)
        assert 1.99 == data["price"]


