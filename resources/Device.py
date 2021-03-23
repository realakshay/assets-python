from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (
    get_jwt_identity, 
    jwt_required
)
from marshmallow import ValidationError
from models.Device import DeviceModel
from models.User import UserModel
from models.Requests import RequestModel
from models.RequestAudit import RequestAuditModel
from models.DeviceAudit import DeviceAuditModel
from models.Locker import LockerModel
from schemas.Device import DeviceSchema
from datetime import date

class DeviceInsert(Resource):

    @classmethod
    @jwt_required
    def post(cls):
        json_data = request.get_json()
        locker_data = LockerModel.find_by_id(json_data['locker_id'])
        if not locker_data.isActivated:
            return {"Message": "Locker is not activate yet"}, 401
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
    @jwt_required
    def get(cls):
        device_data = DeviceModel.find_all()
        return DeviceSchema(many=True).dump(device_data), 201

class AvailableDeviceList(Resource):

    @classmethod
    @jwt_required
    def get(cls):
        device_data = DeviceModel.find_available()
        return DeviceSchema(many=True).dump(device_data), 201

class AssignDeviceToUser(Resource):

    @classmethod
    @jwt_required
    def put(cls, deviceId, userId):
        
        json_data = request.get_json()

        device_data = DeviceModel.find_by_id(deviceId)
        admin_id = get_jwt_identity()

        if device_data.status=="blocked" or device_data.status=="allocated":
            return {"Message": "Device is not available"}, 401
        user_data = UserModel.find_by_id(userId)

        req_obj = {"deviceId": deviceId,"userId":userId}
        request_model = RequestModel(**req_obj)

        device_obj = {"deviceId": deviceId,"userId":userId, "allocateBy": admin_id}
        device_audit_model = DeviceAuditModel(**device_obj)

        admin_data = UserModel.find_by_id(admin_id)

        if device_data and user_data and admin_data.role=="admin":
            # if device_data.status == "created" or device_data.status == "available" :
            if user_data.isActivated:
                if device_data.isActivated :

                    request_model.reqStatus = "approved"
                    device_data.status = "allocated"
                    device_data.assignTo = user_data.email
                    device_data.releaseDate = json_data["releaseDate"]
                    try:
                        device_data.insert_device()
                        request_model.insert_request()
                        # return {"Message": "DEVICE ASSIGNED"}, 201
                    except:
                        return {"Message": "INTERNAL SERVER ERROR"}, 401

                    req_model = RequestModel.get_my_last_request(deviceId, userId)
                    req_audit_obj = {"reqId":req_model.reqId, "handleBy":admin_id}
                    req_audit_model = RequestAuditModel(**req_audit_obj)

                    req_audit_model.insert_request_audit()
                    device_audit_model.insert_device_audit()
                    return {"Message": "DEVICE ASSIGNED"}, 201

                return {"Message": "DEVICE IS NOT ACTIVATED TO ASSIGN"}, 400
            return {"Message": "USER IS NOT ACTIVATED TO ASSIGN"}, 400
        return {"MESSAGE": "INVALID REQUEST"}, 400


class DeallocateDevice(Resource):

    @classmethod
    @jwt_required
    def put(cls, deviceId):
 
        device_data = DeviceModel.find_by_id(deviceId)

        if not device_data:
            return {"Message": "Device Not found"}, 401

        if device_data.assignTo == "0":
            return {"Message": "Device is not allocated"}, 401

        user_data = UserModel.find_by_email(device_data.assignTo)
        device_audit = DeviceAuditModel.find_my_device(deviceId, user_data.id)
        admin_id = get_jwt_identity()

        if device_data.assignTo=="0":
            return {"Message": "Device Not Allocated"}, 403
        if device_data and device_audit:
            # device_data.isAvailable = True
            device_data.status = "available"
            device_data.assignTo = "0"
            device_data.releaseDate = None
            device_audit.deallocateBy = admin_id
            device_audit.deallocateDate = str(date.today().strftime("%d/%m/%Y"))
            try:
                device_data.insert_device()
                device_audit.insert_device_audit()
                return {"Message": "DEVICE DE ALLOCATED"}, 201
            except:
                return {"Message": "INTERNAL SERVER ERROR"}, 401
        return {"MESSAGE": "INVALID REQUEST"}, 400
        


class ActivateDevice(Resource):

    @classmethod
    @jwt_required
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
    @jwt_required
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
    @jwt_required
    def get(cls, deviceId):
        device_data = DeviceModel.find_by_id(deviceId)
        return DeviceSchema().dump(device_data), 201


class AssignedDeviceList(Resource):

    @classmethod
    @jwt_required
    def get(cls):
        assigned_devices = DeviceModel.find_assigned()
        return DeviceSchema(many=True).dump(assigned_devices), 201


class DeviceUpdate(Resource):

    @classmethod
    @jwt_required
    def put(cls, deviceId):
        json_data = request.get_json()
        device_data = DeviceModel.find_by_id(deviceId)
        if device_data:
            device_data.osVersion = json_data['osVersion']
            device_data.rom = json_data['rom']
            device_data.insert_device()
            return {"Message": "Device Updated Successfully"}, 201
        return {"Message": "Internal server error"}, 401

class ActivatedDevices(Resource):

    @classmethod
    @jwt_required
    def get(cls):
        activated_devices = DeviceModel.activated_devices()
        return DeviceSchema(many=True).dump(activated_devices), 201