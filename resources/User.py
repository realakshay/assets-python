from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    get_jwt_identity, 
    jwt_required,
    get_raw_jwt
)
from marshmallow import ValidationError
from werkzeug.security import check_password_hash, generate_password_hash
from models.User import UserModel
from schemas.User import UserSchema
from models.Device import DeviceModel
from schemas.Device import DeviceSchema


class UserResource(Resource):

    @classmethod
    def post(cls):
        json_data = request.get_json()
        print(type(json_data))

        user = UserModel.find_by_email(json_data['email'])
        if user:
            return {"Message": "User with this email is already register"}, 401

        pwd = generate_password_hash(json_data['password'])
        json_data['password'] = pwd

        try:
            user_data = UserSchema().load(json_data)
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
            if data.isActivated:
                if check_password_hash(data.password, json_data['password']):
                # if data.password == json_data['password']:
                    access_token = create_access_token(identity=data.id, fresh=True)
                    refresh_token = create_refresh_token(data.id)
                    user_data = {"role": data.role, "id":data.id, "firstName": data.firstName}
                    return {"Message": "LOGIN_SUCCESS", "data": user_data, "access_token":access_token}, 201
                else :
                    return {"Message" : "INCORRECT_PASSWORD"}, 403
            return {"Message" : "USER_NOT_ACTIVATED_YET"}, 401
        return {"Message" : "USER_NOT_REGISTER"}, 401


class UsersDevices(Resource):

    @classmethod
    @jwt_required
    def get(cls):
        id = get_jwt_identity()
        my_devices = DeviceModel.find_my_devices(id)
        return DeviceSchema(many=True).dump(my_devices), 201


class AllUsers(Resource):

    @classmethod
    @jwt_required
    def get(cls):
        user_data = UserModel.find_all()
        return UserSchema(many=True, exclude=['password']).dump(user_data), 201


class AllActivatedUsers(Resource):

    @classmethod
    @jwt_required
    def get(cls):
        activated_user_data = UserModel.find_all_activated()
        return UserSchema(many=True, exclude=['password']).dump(activated_user_data), 201

class ActivateUser(Resource):

    @classmethod
    @jwt_required
    def post(cls, userId):
    

        user_data = UserModel.find_by_id(userId)
        admin_id = get_jwt_identity()
        admin_data = UserModel.find_by_id(admin_id)

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
    @jwt_required
    def post(cls, userId):


        user_data = UserModel.find_by_id(userId)
        admin_id = get_jwt_identity()
        admin_data = UserModel.find_by_id(admin_id)
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


class EditUser(Resource):

    @classmethod
    @jwt_required
    def put(cls, userId):
        json_data = request.get_json()
        user_data = UserModel.find_by_id(userId)
        if user_data:
            user_data.firstName = json_data['firstName']
            user_data.lastName = json_data['lastName']
            user_data.role = json_data['role']
            user_data.insert_user()
            return {"Message": "User Update Successful"}, 201
        return {"Message": "User Not Found"}, 401
