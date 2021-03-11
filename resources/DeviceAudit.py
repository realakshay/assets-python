from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from models.DeviceAudit import DeviceAuditModel
from schemas.DeviceAudit import DeviceAuditSchema

class AllDeviceAudits(Resource):

    @classmethod
    def get(cls):
        device_audits = DeviceAuditModel.find_all()
        return DeviceAuditSchema(many=True).dump(device_audits), 201