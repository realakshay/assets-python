from db import db
from datetime import date

class DeviceAuditModel(db.Model):

    __tablename__ = "device_audit"

    id = db.Column(db.Integer, primary_key=True)
    deviceId = db.Column(db.Integer, db.ForeignKey("my_devices.id"), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey("atos_users.id"), nullable=False)
    allocateDate = db.Column(db.String(100), default=date.today().strftime("%d/%m/%Y"))
    allocateBy = db.Column(db.Integer, db.ForeignKey("atos_users.id"), nullable=False)
    deallocateDate = db.Column(db.String(100), default=None)
    deallocateBy = db.Column(db.Integer, db.ForeignKey("atos_users.id"), default=None)

    device = db.relationship("DeviceModel")
    user = db.relationship("UserModel", foreign_keys=[userId])
    allocate_by = db.relationship("UserModel", foreign_keys=[allocateBy])
    deallocate_by = db.relationship("UserModel", foreign_keys=[deallocateBy])


    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_my_device(cls, deviceId, userId):
        return cls.query.filter((cls.deviceId==deviceId)&(cls.userId==userId)).order_by(db.desc(cls.id)).first()
    
    def insert_device_audit(self):
        db.session.add(self)
        db.session.commit()