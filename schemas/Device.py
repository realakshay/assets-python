from marshmallow import Schema, fields
from models.Device import DeviceModel

class DeviceSchema(Schema):
    class meta:
        model = DeviceModel

    id = fields.Int(dump_only=True)
    deviceName = fields.Str()
    deviceType = fields.Str()
    company = fields.Str()
    imei = fields.Int()
    osVersion = fields.Str()
    os = fields.Str()
    ram = fields.Str()
    rom = fields.Str()
    isActivated = fields.Bool()
    # isAvailable = fields.Bool()
    releaseDate = fields.Str(dump_only=True)
    assignTo = fields.Str()
    status = fields.Str()

    locker_id = fields.Int()