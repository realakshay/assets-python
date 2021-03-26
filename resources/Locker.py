from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (
    get_jwt_identity, 
    jwt_required
)
from marshmallow import ValidationError
from models.Locker import LockerModel
from schemas.Locker import LockerSchema

class Locker(Resource):

    @classmethod
    @jwt_required
    def get(cls):
        locker_data = LockerModel.find_all_locker()
        return LockerSchema(many=True).dump(locker_data), 201


    @classmethod
    @jwt_required
    def post(cls):
        json_data = request.get_json()

        try:
            locker_data = LockerSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 401

        try:
            locker_model = LockerModel(**locker_data)
            locker_model.insert_locker()
            return {"Message": "Locker Inserted"}, 201
        except:
            return {"Message": "Error While Insertion"}, 401

class ActivatedLocker(Resource):
    
    @classmethod
    @jwt_required
    def get(cls):
        activated_lockers = LockerModel.find_activated()
        return LockerSchema(many=True).dump(activated_lockers), 201


class ActivateLocker(Resource):

    @classmethod
    @jwt_required
    def put(cls, lockerId):
        locker_data = LockerModel.find_by_id(lockerId)

        if not locker_data:
            return {"Message": "Locker not found"}, 401

        if locker_data.isActivated:
            return {"Message": "Locker is already activated"}, 401
        locker_data.isActivated = True
        try:
            locker_data.insert_locker()
            return {"Message": "Locker activated successful"}, 201
        except:
            return {"Message": "Internal server error"}, 401


class DeActivateLocker(Resource):

    @classmethod
    @jwt_required
    def put(cls, lockerId):
        locker_data = LockerModel.find_by_id(lockerId)

        if not locker_data:
            return {"Message": "Locker not found"}, 401

        if not locker_data.isActivated:
            return {"Message": "Locker is already deactivated"}, 401

        jumble_data = LockerSchema().dump(locker_data)
        if len(jumble_data['devices'])>0:
            return {"Message": "This locker holds some devices"}, 401
        locker_data.isActivated = False
        try:
            locker_data.insert_locker()
            return {"Message": "Locker de-activated successful"}, 201
        except:
            return {"Message": "Internal server error"}, 401


class EditLocker(Resource):

    @classmethod
    @jwt_required
    def put(cls, lockerId):
        json_data = request.get_json()
        locker_data = LockerModel.find_by_id(lockerId)
        if not locker_data:
            return {"Message": "Locker with this id not found"}, 401
        locker_data.name = json_data['name']
        locker_data.description = json_data['description']
        locker_data.insert_locker()
        return {"Message": "Locker updated"}, 201
