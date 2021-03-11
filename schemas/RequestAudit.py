from marshmallow import Schema, fields
from models.RequestAudit import RequestAuditModel
from schemas.User import UserSchema
from schemas.Requests import RequestSchema

class RequestAuditSchema(Schema):
    class Meta:
        model = RequestAuditModel

    id = fields.Int(dump_only=True)
    reqId = fields.Int(dump_only=True)
    handleBy = fields.Int()
    handleDate = fields.DateTime(dump_only=True)

    request = fields.Nested(RequestSchema)
    requestHandler = fields.Nested(UserSchema(exclude=['password']))
    