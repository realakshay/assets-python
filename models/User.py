from db import db

class UserModel(db.Model):
    __tablename__ = "atos_users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    devices = db.Column(db.ARRAY(db.String), default=[])

    

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    def insert_user(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_user(self):
        db.session.delete(self)
        db.session.commit()