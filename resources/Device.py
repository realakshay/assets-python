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
            if device_data.isActivated :
                device_data.isAvailable = False
                device_data.assignTo = userId
                try:
                    device_data.insert_device()
                    return {"Message": "DEVICE ASSIGNED"}, 201
                except:
                    return {"Message": "INTERNAL SERVER ERROR"}, 401
            return {"Message": "DEVICE IS NOT ACTIVATED TO ASSIGN"}, 400
        return {"MESSAGE": "INVALID REQUEST"}, 400


class DeallocateDevice(Resource):

    @classmethod
    def put(cls, deviceId, userId):
        device_data = DeviceModel.find_by_id(deviceId)
        if device_data:
            device_data.isAvailable = True
            device_data.assignTo = 0
            try:
                device_data.insert_device()
                return {"Message": "DEVICE DE ALLOCATED"}, 201
            except:
                return {"Message": "INTERNAL SERVER ERROR"}, 401
        return {"MESSAGE": "INVALID REQUEST"}, 400
        


class ActivateDevice(Resource):

    @classmethod
    def put(cls, deviceId):
        device_data = DeviceModel.find_by_id(deviceId)
        if device_data:
            device_data.isActivated = True
            try:
                device_data.insert_device()
                return {"Message": "DEVICE ACTIVATED"}, 201
            except:
                return {"Message": "INTERNAL SERVER ERROR"}, 401
        return {"MESSAGE": "INVALID REQUEST"}, 400


class DeActivateDevice(Resource):

    @classmethod
    def put(cls, deviceId):
        device_data = DeviceModel.find_by_id(deviceId)
        if device_data:
            device_data.isActivated = False
            try:
                device_data.insert_device()
                return {"Message": "DEVICE DE ACTIVATED"}, 201
            except:
                return {"Message": "INTERNAL SERVER ERROR"}, 401
        return {"MESSAGE": "INVALID REQUEST"}, 400


class SpecificDevice(Resource):

    @classmethod
    def get(cls, deviceId):
        device_data = DeviceModel.find_by_id(deviceId)
        return DeviceSchema().dump(device_data), 201
