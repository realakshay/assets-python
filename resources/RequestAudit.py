from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from models.RequestAudit import RequestAuditModel
from schemas.RequestAudit import RequestAuditSchema


class AllRequsetAudits(Resource):

    @classmethod
    def get(cls):
        request_audits = RequestAuditModel.find_all()
        return RequestAuditSchema(many=True).dump(request_audits), 201