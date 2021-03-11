from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from models.Device import DeviceModel
from models.User import UserModel
from models.Requests import RequestModel
from models.RequestAudit import RequestAuditModel
from models.DeviceAudit import DeviceAuditModel
from schemas.Device import DeviceSchema
from datetime import date

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
        
        json_data = request.get_json()

        device_data = DeviceModel.find_by_id(deviceId)
        user_data = UserModel.find_by_id(userId)

        req_obj = {"deviceId": deviceId,"userId":userId}
        request_model = RequestModel(**req_obj)

        device_obj = {"deviceId": deviceId,"userId":userId, "allocateBy": json_data["admin_id"]}
        device_audit_model = DeviceAuditModel(**device_obj)

        admin_data = UserModel.find_by_id(json_data['admin_id'])

        if device_data and user_data and admin_data.role=="admin":
            # if device_data.status == "created" or device_data.status == "available" :
            if user_data.isActivated:
                if device_data.isActivated :
                    # device_data.isAvailable = False
                    # if user_data.role == "admin":
                    request_model.reqStatus = "approved"
                    device_data.status = "allocated"
                    device_data.assignTo = user_data.email
                    try:
                        device_data.insert_device()
                        request_model.insert_request()
                        # return {"Message": "DEVICE ASSIGNED"}, 201
                    except:
                        return {"Message": "INTERNAL SERVER ERROR"}, 401

                    req_model = RequestModel.get_my_last_request(deviceId, userId)
                    req_audit_obj = {"reqId":req_model.reqId, "handleBy":json_data["admin_id"]}
                    req_audit_model = RequestAuditModel(**req_audit_obj)

                    try:
                        req_audit_model.insert_request_audit()
                        device_audit_model.insert_device_audit()
                        return {"Message": "DEVICE ASSIGNED"}, 201
                        
                    except:
                        return {"Message": "INTERNAL SERVER ERROR"}, 403

                    
                # return {"Message": "DEVICE ALREADY ASSIGNED TO USER"}, 403
                return {"Message": "DEVICE IS NOT ACTIVATED TO ASSIGN"}, 400
            return {"Message": "USER IS NOT ACTIVATED TO ASSIGN"}, 400
        return {"MESSAGE": "INVALID REQUEST"}, 400


class DeallocateDevice(Resource):

    @classmethod
    def put(cls, deviceId, userId):
        json_data = request.get_json()
        device_data = DeviceModel.find_by_id(deviceId)
        device_audit = DeviceAuditModel.find_my_device(deviceId, userId)
        if device_data and device_audit:
            # device_data.isAvailable = True
            device_data.status = "available"
            device_data.assignTo = "0"
            device_audit.deallocateBy = json_data['admin_id']
            device_audit.deallocateDate = date.today().strftime("%d/%m/%Y")
            try:
                device_data.insert_device()
                device_audit.insert_device_audit()
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
        return {"MESSAGE": "INVALID REQUEST"}, 401


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