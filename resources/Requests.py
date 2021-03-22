from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (
    get_jwt_identity, 
    jwt_required
)
from marshmallow import ValidationError
from models.Requests import RequestModel
from schemas.Requests import RequestSchema
from schemas.RequestAudit import RequestAuditSchema

from models.User import UserModel
from models.Device import DeviceModel
from models.RequestAudit import RequestAuditModel
from models.DeviceAudit import DeviceAuditModel

request_schema = RequestSchema()
requests_schema = RequestSchema(many=True)

class RegisterRequest(Resource):

    @classmethod
    @jwt_required
    def post(cls):
        json_data = request.get_json()
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        device = DeviceModel.find_by_id(json_data["deviceId"])

        print(json_data["releaseDate"])

        if device.status=="available" or device.status=="created":
            if user and device:
                if device.isActivated :
                    if device.status=="created" or device.status=="available":
                        try:
                            req_obj = {"deviceId" : json_data["deviceId"], "userId" : user.id}
                            request_data = request_schema.load(req_obj)
                        except ValidationError as err:
                            return err.messages, 401

                        try:
                            request_model = RequestModel(**request_data)
                            device.status = "blocked"
                            device.releaseDate = json_data["releaseDate"]
                            request_model.insert_request()
                            device.insert_device()
                        except:
                            return {"Message" : "REQUEST INSERT ERROR"}, 401
                        return {"Message" : "REQUEST SUCCESSFULLY ADDED"}, 201
                    return {"Message" : "DEVICE IS NOT AVAILABLE"}, 401
                return {"Message" : "DEVICE IS NOT ACTIVATED"}, 401
            return {"Message" : "SOMETHING GETTING WRONG"}, 401
        return {"Messgae": "Device is not available to request"}, 401


class AllPendingRequests(Resource):

    @classmethod
    @jwt_required
    def get(cls):
        pending_requests = RequestModel.find_pending()
        return requests_schema.dump(pending_requests), 201


class ApproveRequest(Resource):

    @classmethod
    @jwt_required
    def put(cls, reqId):

        
        admin_id = get_jwt_identity()
        request_data = RequestModel.find_by_id(reqId)
        device_data = DeviceModel.find_by_id(request_data.deviceId)

        if request_data.reqStatus == "pending":
            if device_data.status=="blocked":
                user_data = UserModel.find_by_id(request_data.userId)
                req_audit_obj = {"reqId":reqId, "handleBy": admin_id}
                req_audit_model = RequestAuditModel(**req_audit_obj)

                device_obj = {
                    "deviceId": request_data.deviceId,
                    "userId": request_data.userId, 
                    "allocateBy": admin_id
                }
                device_audit_model = DeviceAuditModel(**device_obj)

                admin_data = UserModel.find_by_id(admin_id)
                
                if request_data and admin_data.role=="admin":
                    request_data.reqStatus = "approved"
                    device_data.status = "allocated"
                    device_data.assignTo = user_data.email
                    request_data.insert_request()
                    device_data.insert_device()
                    req_audit_model.insert_request_audit()
                    device_audit_model.insert_device_audit()
                    return {"Message": "Request Approved"}, 201
                return {"Message": "Request Not Found"}, 401
            return {"Message": "Device is not requested"}, 401
        return {"Message": "Request Already Resolve"}, 403



class DeclineRequest(Resource):

    @classmethod
    @jwt_required
    def put(cls, reqId):

        
        admin_id = get_jwt_identity()
        request_data = RequestModel.find_by_id(reqId)
        if request_data.reqStatus == "pending":
            device_data = DeviceModel.find_by_id(request_data.deviceId)
            user_data = UserModel.find_by_id(request_data.userId)

            req_audit_obj = {"reqId":reqId, "handleBy":admin_id}
            req_audit_model = RequestAuditModel(**req_audit_obj)

            admin_data = UserModel.find_by_id(admin_id)

            if request_data and admin_data.role=="admin":
                request_data.reqStatus = "declined"
                device_data.status = "available"
                device_data.assignTo = "0"
                device_data.releaseDate = None
                request_data.insert_request()
                device_data.insert_device()
                req_audit_model.insert_request_audit()
                # declined request
                return {"Message": "Request Declined Successfully"}, 201
            return {"Message": "Request Not Found"}, 401
        return {"Message": "Request Already Resolve"}, 403


class AllMyRequests(Resource):

    @classmethod
    @jwt_required
    def get(cls):
        user_id = get_jwt_identity()
        my_requests = RequestModel.find_my_requests(user_id)
        return requests_schema.dump(my_requests), 201