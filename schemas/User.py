from marshmallow import Schema, fields
from models.User import UserModel

class UserSchema(Schema):
    class meta:
        model = UserModel
    id = fields.Int(dump_only=True)
    username = fields.Str()
    password = fields.Str()
    email = fields.Str()
    # devices = fields.List(fields.Str())
    first_name = fields.Str()
    last_name = fields.Str()
    role = fields.Str()

    isActivated = fields.Bool()