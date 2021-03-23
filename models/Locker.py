from db import db

class LockerModel(db.Model):

    __tablename__ = "locker"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    devices = db.relationship('DeviceModel', lazy="dynamic")

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all_locker(cls):
        return cls.query.all()

    def insert_locker(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_locker(self):
        db.session.delete(self)
        db.session.commit()