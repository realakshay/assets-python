from marshmallow import Schema, fields
from models.DeviceAudit import DeviceAuditModel
from schemas.Device import DeviceSchema
from schemas.User import UserSchema

class DeviceAuditSchema(Schema):
    class Meta:
        model = DeviceAuditModel

    id = fields.Int(dump_only=True)
    deviceId = fields.Int()
    userId = fields.Int()
    allocateDate = fields.DateTime(dump_only=True)
    allocateBy = fields.Int()
    deallocateDate = fields.DateTime(dump_only=True)
    deallocateBy = fields.Int()

    device = fields.Nested(DeviceSchema)
    user = fields.Nested(UserSchema(exclude=['password']))
    allocate_by = fields.Nested(UserSchema(exclude=['password']))
    deallocate_by = fields.Nested(UserSchema(exclude=['password']))
    