from db import db


class UserModel(db.Model):
    __tablename__ = "atos_users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    # devices = db.Column(db.ARRAY(db.String), default=[])
    role = db.Column(db.String(100), nullable=False)

    firstName = db.Column(db.String(200), nullable=False)
    lastName = db.Column(db.String(200), nullable=False)

    isActivated = db.Column(db.Boolean, default=False)
    requests = db.relationship('RequestModel', lazy='dynamic')
    request_audit = db.relationship('RequestAuditModel', lazy='dynamic')

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_all_activated(cls):
        return cls.query.filter_by(isActivated=True).all()
    
    def insert_user(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_user(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()