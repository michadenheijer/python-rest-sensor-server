from flask import Flask
from flask_restful import Api, Resource, reqparse

try:
    import tsl2591
    tsl2591 = tsl2591.Tsl2591()
except ImportError:
    print("Cannot import lux_sensor")
except Exception as error:
    print(error)

try:
    import Adafruit_MCP9808.MCP9808 as MCP9808
    mcp9808 = MCP9808.MCP9808(busnum=0)
    mcp9808.begin()
except ImportError:
    print("Cannot import temp_sensor")
except Exception as error:
    print(error)


app = Flask(__name__)
api = Api(app)


class cpu(Resource):
    def get(self):
        try:
            tempFile = open('/sys/devices/virtual/thermal/thermal_zone0/temp').read()
            temp = int(float(tempFile)/100)/10
            return temp, 200
        except Exception as error:
            print(error)
            return "Server error", 500

class temp(Resource):
    def get(self):
        try:
            temp = int(mcp9808.readTempC()*10-16)/10
            return temp, 200
        except Exception as error:
            print(error)
            return "Server error", 500

class lux(Resource):
    def get(self):
        try:
            full, ir = tsl2591.get_full_luminosity()
            lux = int(tsl2591.calculate_lux(full, ir)*10)/10
            return lux, 200
        except Exception as error:
            return "Server error", 500

@app.errorhandler(404)
def does_not_exist(Resource):
    return "Does not exist\n", 404

api.add_resource(cpu, "/cpu")
api.add_resource(temp, "/temp")
api.add_resource(lux, "/lux")

app.run(host='0.0.0.0')
