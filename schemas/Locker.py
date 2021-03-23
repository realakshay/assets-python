from marshmallow import Schema, fields
from models.Locker import LockerModel
from schemas.Device import DeviceSchema

class LockerSchema(Schema):
    class meta:
        model = LockerModel
    
    id = fields.Int(dump_only=True)
    name = fields.Str()
    description = fields.Str()
    isActivated = fields.Bool()
    devices = fields.Nested(DeviceSchema(many=True))