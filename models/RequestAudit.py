from db import db
from datetime import date

class RequestAuditModel(db.Model):

    __tablename__ = "request_audit"

    id = db.Column(db.Integer, primary_key=True)
    reqId = db.Column(db.Integer, db.ForeignKey("requests.reqId"), nullable=False)
    handleBy = db.Column(db.Integer, db.ForeignKey("atos_users.id"), nullable=False)
    handleDate = db.Column(db.String(100), default=date.today().strftime("%d/%m/%Y"))

    request = db.relationship("RequestModel")
    requestHandler = db.relationship("UserModel")


    @classmethod
    def find_by_reqId(cls, reqId):
        return cls.query.filter_by(reqId=reqId).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    def insert_request_audit(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_request_audit(self):
        db.session.delete(self)
        db.session.commit()