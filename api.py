from flask import Flask
from flask_restful import Api, Resource, reqparse

try:
    from tsl2561 import TSL2561
    tsl = TSL2561(debug=True)
except ImportError:
    print("Cannot import lux_sensor")
except Exception as error:
    print(error)

try:
    import Adafruit_MCP9808.MCP9808 as MCP9808
    sensor = MCP9808.MCP9808()
    sensor.begin()
except ImportError:
    print("Cannot import temp_sensor")
except Exception as error:
    print(error)


app = Flask(__name__)
api = Api(app)


class cpu(Resource):
    def get(self):
        tempFile = open('/sys/devices/virtual/thermal/thermal_zone0/temp').read()
        temp = int(float(tempFile)/1000)
        return temp, 200

api.add_resource(cpu, "/cpu")

app.run(debug=True, host='0.0.0.0')
