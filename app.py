import os
from db import db
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from dotenv import load_dotenv
from resources.User import UserResource, UserLogin
from resources.Device import DeviceInsert, DeviceList, AvailableDeviceList

load_dotenv('.env')

app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY')
CORS(app)

api = Api(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

@app.before_first_request
def create_tables():
    db.drop_all()
    db.create_all()

@app.route('/')
def method_name():
    return "<h1>App is running now</h1>"

api.add_resource(UserResource, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(DeviceInsert, '/device/insert')
api.add_resource(DeviceList, '/devices')
api.add_resource(AvailableDeviceList, '/device/available')

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(debug=True)