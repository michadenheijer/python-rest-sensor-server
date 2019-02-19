from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

class Cpu(Resource):
    def get(self):
        tempFile = open('/sys/devices/virtual/thermal/thermal_zone0/temp').read()
        temp = int(float(tempFile)/1000)
        return temp, 200

api.add_resource(Cpu, "/cpu")

app.run(debug=True, host='0.0.0.0')
