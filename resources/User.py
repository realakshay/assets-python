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
            "email" : json_data["email"],
            "role": json_data["role"],
            "firstName": json_data["firstName"],
            "lastName": json_data["lastName"]
        }

        try:
            user_data = UserSchema().load(personal_info)
            print(user_data)
        except ValidationError as err:
            return err.messages, 401

        try:
            user_model = UserModel(**user_data)
            if user_model.role=="admin":
                user_model.isActivated = True
                user_model.insert_user()
            else:
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
                return { "Message": "LOGIN_SUCCESS", "role": data.role}, 201
            else :
                return {"Message" : "INCORRECT_PASSWORD"}, 403
        return {"Message" : "USER_NOT_REGISTER"}, 401


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


class ActivateUser(Resource):

    @classmethod
    def post(cls, userId):
        json_data = request.get_json()

        user_data = UserModel.find_by_id(userId)
        admin_data = UserModel.find_by_id(json_data['admin_id'])

        if user_data:
            if admin_data:
                if admin_data.role=="admin":
                    if not user_data.isActivated:
                        user_data.isActivated = True
                        user_data.insert_user()
                        return {"Message": "User is Activated"}, 201
                    return {"Message": "User is Already Activated"}, 201
                return {"Message": "You dont have an access to activate other user"}, 401
            return {"Message": "Admin Not Found"}, 401
        return {"Message": "User Not Found"}, 401


class DeActivateUser(Resource):

    @classmethod
    def post(cls, userId):
        json_data = request.get_json()

        user_data = UserModel.find_by_id(userId)
        admin_data = UserModel.find_by_id(json_data['admin_id'])
        user_devices = DeviceModel.find_my_devices(userId)
        type(user_devices)
        print(len(user_devices))
        if user_data:
            if len(user_devices)==0:
                if admin_data:
                    if admin_data.role=="admin":
                        if user_data.isActivated:
                            user_data.isActivated = False
                            user_data.insert_user()
                            return {"Message": "User is DeActivated"}, 201
                        return {"Message": "User is Already DeActivated"},401
                    return {"Message": "You dont have an access to deactivate other user"}, 401
                return {"Message": "Admin Not Found"}, 401
            return {"Message": "User has some devices so you cannot deactivate him"}, 401
        return {"Message": "User Not Found"}, 401