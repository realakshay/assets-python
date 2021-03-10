from db import db
from datetime import date

class RequestModel(db.Model):

    __tablename__ = "requests"

    reqId = db.Column(db.Integer, primary_key=True)
    reqDate = db.Column(db.Date, default=date.today().strftime("%d/%m/%Y"))
    deviceId = db.Column(db.Integer, db.ForeignKey("my_devices.id"), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey("atos_users.id"), nullable=False)
    reqStatus = db.Column(db.String(100), default="pending")

    # handle_by
    # handle_date

    device = db.relationship("DeviceModel")
    user = db.relationship("UserModel")


    @classmethod
    def find_pending(cls):
        return cls.query.filter_by(reqStatus="pending").all()
    
    def insert_request(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_request(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, reqId):
        return cls.query.filter_by(reqId=reqId).first()