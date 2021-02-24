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

class AvailableDeviceList(Resource):

    @classmethod
    def get(cls):
        device_data = DeviceModel.find_available()
        return DeviceSchema(many=True).dump(device_data), 201

class AssignDeviceToUser(Resource):

    @classmethod
    def put(cls, deviceId, userId):
        device_data = DeviceModel.find_by_id(deviceId)
        if device_data:
            device_data.isAvailable = False
            device_data.assignTo = userId
            try:
                device_data.insert_device()
                return {"Message": "DEVICE ASSIGNED"}, 201
            except:
                return {"Message": "INTERNAL SERVER ERROR"}, 201
        return {"MESSAGE": "INVALID REQUEST"}, 400