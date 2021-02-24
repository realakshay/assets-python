from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from models.Device import DeviceModel
from schemas.Device import DeviceSchema

class DeviceInsert(Resource):

    @classmethod
    def post(cls):
        json_data = request.get_json()
        
        try:
            device_data = DeviceSchema().load(json_data)
            print(device_data)
        except ValidationError as err:
            return err.messages, 401

        try:
            device_model = DeviceModel(**device_data)
            device_model.insert_device()
        except:
            return {"Message" : "DEVICE_INSERTION_ERROR"}, 401
        return {"Message" : "DEVICE_REGISTRATION_SUCCESSFUL"}, 201


class DeviceList(Resource):

    @classmethod
    def get(cls):
        device_data = DeviceModel.find_all()
        return DeviceSchema(many=True).dump(device_data), 201
