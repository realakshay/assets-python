from marshmallow import Schema, fields
from models.Requests import RequestModel
from schemas.Device import DeviceSchema
from schemas.User import UserSchema

class RequestSchema(Schema):
    class Meta:
        model = RequestModel
    reqId = fields.Int(dump_only=True)
    reqDate = fields.DateTime(dump_only=True)
    deviceId = fields.Int()
    userId = fields.Int()
    reqStatus = fields.Str(dump_only=True)

    device = fields.Nested(DeviceSchema)
    user = fields.Nested(UserSchema(exclude=['password']))
    