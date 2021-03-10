from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from models.Device import DeviceModel
from models.User import UserModel
from models.Requests import RequestModel
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
        user_data = UserModel.find_by_id(userId)
        request_model = RequestModel({"deviceId": deviceId,"userId":userId})
        if device_data and user_data:
            if device_data.isActivated :
                # device_data.isAvailable = False
                if user_data.role == "admin":
                    request_model.reqStatus = "approved"
                device_data.status = "allocated"
                device_data.assignTo = user_data.email
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
            # device_data.isAvailable = True
            device_data.status = "available"
            device_data.assignTo = "0"
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
            if device_data.assignTo != "0":
                return {"Message": "DEVICE IS ASSIGNED TO SOMEONE"}, 401
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


class AssignedDeviceList(Resource):

    @classmethod
    def get(cls):
        assigned_devices = DeviceModel.find_assigned()
        return DeviceSchema(many=True).dump(assigned_devices), 201


class DeviceUpdate(Resource):

    @classmethod
    def put(cls, deviceId):
        json_data = request.get_json()
        device_data = DeviceModel.find_by_id(deviceId)
        if device_data:
            device_data.osVersion = json_data['osVersion']
            device_data.rom = json_data['rom']
            device_data.insert_device()
            return {"Message": "Device Updated Successfully"}, 201
        return {"Message": "Internal server error"}, 401