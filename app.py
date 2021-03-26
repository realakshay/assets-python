import os
from db import db
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from resources.User import (
    UserResource, 
    UserLogin, 
    UsersDevices, 
    AllUsers,
    ActivateUser,
    DeActivateUser,
    AllActivatedUsers,
    EditUser
)
from resources.Device import (
    DeviceInsert, 
    DeviceList, 
    AvailableDeviceList, 
    AssignDeviceToUser,
    DeallocateDevice,
    ActivateDevice,
    DeActivateDevice,
    SpecificDevice,
    AssignedDeviceList,
    DeviceUpdate,
    ActivatedDevices
)

from resources.Requests import (
    RegisterRequest, 
    AllPendingRequests,
    ApproveRequest,
    DeclineRequest,
    AllMyRequests
)

from resources.RequestAudit import AllRequsetAudits
from resources.DeviceAudit import AllDeviceAudits

from resources.Locker import Locker, ActivatedLocker, ActivateLocker, DeActivateLocker, EditLocker

load_dotenv('.env')

app = Flask(__name__)

app.secret_key = os.getenv('APP_SECRET_KEY')
CORS(app)
JWTManager(app)
api = Api(app)

app.config['SECRET_KEY'] =os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

@app.before_first_request
def create_tables():
    db.drop_all()
    db.create_all()

@app.route('/')
def home():
    return "<h1>App is running now</h1>"

api.add_resource(DeviceInsert, '/device/insert')
api.add_resource(DeviceList, '/devices')
api.add_resource(AvailableDeviceList, '/device/available')
api.add_resource(UsersDevices, '/mydevices')
api.add_resource(AssignDeviceToUser, '/assign/<int:deviceId>/<int:userId>')
api.add_resource(DeallocateDevice, '/deallocate/<int:deviceId>')
api.add_resource(ActivateDevice, '/activate/<int:deviceId>')
api.add_resource(DeActivateDevice, '/deactivate/<int:deviceId>')
api.add_resource(SpecificDevice, '/getdevice/<int:deviceId>')
api.add_resource(AssignedDeviceList, '/all/assigned')
api.add_resource(DeviceUpdate, '/update/device/<int:deviceId>')
api.add_resource(ActivatedDevices, '/devices/activated')


# Request Session will goes here

api.add_resource(RegisterRequest, "/insert/request")
api.add_resource(AllPendingRequests, "/requests/pending")
api.add_resource(ApproveRequest, "/request/approve/<int:reqId>")
api.add_resource(DeclineRequest, "/request/decline/<int:reqId>")
api.add_resource(AllMyRequests, "/myrequests")


# Request Audits goes here
api.add_resource(AllRequsetAudits, "/request/audits")

# Device Audit goes here
api.add_resource(AllDeviceAudits, "/device/audits")

# user requests
api.add_resource(ActivateUser, "/user/activate/<int:userId>")
api.add_resource(DeActivateUser, "/user/deactivate/<int:userId>")
api.add_resource(AllActivatedUsers, "/users/activated")
api.add_resource(UserResource, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(AllUsers, '/allusers')
api.add_resource(EditUser, "/user/edit/<int:userId>")


# Locker requests
api.add_resource(Locker, "/locker")
api.add_resource(ActivatedLocker, "/locker/activated")
api.add_resource(ActivateLocker, "/locker/activate/<int:lockerId>")
api.add_resource(DeActivateLocker, "/locker/deactivate/<int:lockerId>")
api.add_resource(EditLocker, "/locker/edit/<int:lockerId>")

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(debug=True)