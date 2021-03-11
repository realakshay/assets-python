import os
from db import db
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from dotenv import load_dotenv
from resources.User import UserResource, UserLogin, UsersDevices, AllUsers
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
    DeviceUpdate
)

from resources.Requests import (
    RegisterRequest, 
    AllPendingRequests,
    ApproveRequest,
    DeclineRequest
)

from resources.RequestAudit import AllRequsetAudits

from resources.DeviceAudit import AllDeviceAudits

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
api.add_resource(UsersDevices, '/mydevices/<int:id>')
api.add_resource(AssignDeviceToUser, '/assign/<int:deviceId>/<int:userId>')
api.add_resource(DeallocateDevice, '/deallocate/<int:deviceId>/<string:userId>')
api.add_resource(ActivateDevice, '/activate/<int:deviceId>')
api.add_resource(DeActivateDevice, '/deactivate/<int:deviceId>')
api.add_resource(SpecificDevice, '/getdevice/<int:deviceId>')
api.add_resource(AllUsers, '/allusers')
api.add_resource(AssignedDeviceList, '/all/assigned')
api.add_resource(DeviceUpdate, '/update/device/<int:deviceId>')


# Request Session will goes here

api.add_resource(RegisterRequest, "/insert/request")
api.add_resource(AllPendingRequests, "/requests/pending")
api.add_resource(ApproveRequest, "/request/approve/<int:reqId>")
api.add_resource(DeclineRequest, "/request/decline/<int:reqId>")


# Request Audits goes here
api.add_resource(AllRequsetAudits, "/request/audits")

# Device Audit goes here
api.add_resource(AllDeviceAudits, "/device/audits")

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(debug=True)