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