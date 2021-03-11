from db import db
from models.User import UserModel

class DeviceModel(db.Model):
    __tablename__ = "my_devices"

    id = db.Column(db.Integer, primary_key=True)
    deviceName = db.Column(db.String(100), nullable=False)
    deviceType = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    imei = db.Column(db.BigInteger)
    osVersion = db.Column(db.String(100), nullable=False)
    os = db.Column(db.String(100), nullable=False)
    ram = db.Column(db.String(100), nullable=False)
    rom = db.Column(db.String(100), nullable=False)
    isActivated = db.Column(db.Boolean, default=False)
    # isAvailable = db.Column(db.Boolean, default=True)
    releaseDate = db.Column(db.String(100), nullable=False, default="01/01/2020")
    assignTo = db.Column(db.String(100), default="0")

    # status could be created, allocated, available, blocked
    status = db.Column(db.String(100), default="created")

    requests=db.relationship('RequestModel',lazy='dynamic')
    
    @classmethod
    def find_by_id(cls, id: int) -> "DeviceModel":
        return cls.query.filter_by(id=id).first()

    # @classmethod
    # def find_available(cls):
    #     return cls.query.filter_by(isAvailable=True).all()

    @classmethod
    def find_available(cls):
        return cls.query.filter((cls.status=="created")|(cls.status=="available")).all()

    @classmethod
    def find_assigned(cls):
        return cls.query.filter(cls.assignTo != "0").all()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_my_devices(cls, userId):
        user_data = UserModel.find_by_id(userId)
        return cls.query.filter_by(assignTo=user_data.email).all()

    def insert_device(self):
        db.session.add(self)
        db.session.commit()

    def delete_device(self):
        db.session.delete(self)
        db.session.commit()