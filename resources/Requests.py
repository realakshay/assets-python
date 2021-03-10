from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from models.Requests import RequestModel
from schemas.Requests import RequestSchema

from models.User import UserModel
from models.Device import DeviceModel

request_schema = RequestSchema()
requests_schema = RequestSchema(many=True)

class RegisterRequest(Resource):

    @classmethod
    def post(cls):
        json_data = request.get_json()
        user = UserModel.find_by_id(json_data["userId"])
        device = DeviceModel.find_by_id(json_data["deviceId"])

        if user and device:
            if device.status=="created" or device.status=="available":
                try:
                    request_data = request_schema.load(json_data)
                except ValidationError as err:
                    return err.messages, 401

                try:
                    request_model = RequestModel(**request_data)
                    device.status = "blocked"
                    request_model.insert_request()
                    device.insert_device()
                except:
                    return {"Message" : "REQUEST INSERT ERROR"}, 401
                return {"Message" : "REQUEST SUCCESSFULLY ADDED"}, 201
            return {"Message" : "DEVICE IS NOT AVAILABLE"}, 401
        return {"Message" : "SOMETHING GETTING WRONG"}, 401


class AllPendingRequests(Resource):

    @classmethod
    def get(cls):
        pending_requests = RequestModel.find_pending()
        return requests_schema.dump(pending_requests), 201


class ApproveRequest(Resource):

    @classmethod
    def put(cls, reqId):
        request_data = RequestModel.find_by_id(reqId)
        device_data = DeviceModel.find_by_id(request_data.deviceId)
        user_data = UserModel.find_by_id(request_data.userId)
        if request_data:
            request_data.reqStatus = "approved"
            device_data.status = "allocated"
            device_data.assignTo = user_data.email
            request_data.insert_request()
            device_data.insert_device()
            return {"Message": "Request Approved"}, 201
        return {"Message": "Request Not Found"}, 401