from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from models.User import UserModel
from schemas.User import UserSchema
from models.Device import DeviceModel
from schemas.Device import DeviceSchema


class UserResource(Resource):

    @classmethod
    def post(cls):
        json_data = request.get_json()
        print(type(json_data))

        personal_info = {
            "username" : json_data["username"],
            "password" : json_data["password"],
            "email" : json_data["email"]
        }
        print(personal_info)
        try:
            user_data = UserSchema().load(personal_info)
            print(user_data)
        except ValidationError as err:
            return err.messages, 401

        try:
            user_model = UserModel(**user_data)
            user_model.insert_user()
        except:
            return {"Message" : "USER_INSERTION_ERROR"}, 401
        return {"Message" : "USER_REGISTRATION_SUCCESSFUL"}, 201


class UserLogin(Resource):
    
    @classmethod
    def post(cls):
        json_data = request.get_json()
        data = UserModel.find_by_username(json_data['username'])
        if data :
            if data.password == json_data['password']:
                return { "Message": "LOGIN_SUCCESS"}, 201
            else :
                return {"Message" : "INCORRECT_PASSWORD"}, 403
        return {"Message" : "USER_NOT_REGISTER"}, 


class UsersDevices(Resource):

    @classmethod
    def get(cls, id : int):
        my_devices = DeviceModel.find_my_devices(id)
        return DeviceSchema(many=True).dump(my_devices), 201


class AllUsers(Resource):

    @classmethod
    def get(cls):
        user_data = UserModel.find_all()
        return UserSchema(many=True, exclude=['password']).dump(user_data), 201