from flask import Flask
from waitress import serve
from flask_restful import Api, Resource, reqparse

import subprocess
import sys

try:
    if str(open('/sys/firmware/devicetree/base/model').read()) == 'Xunlong Orange Pi Zero\x00':
        device = 'OrangePiZero'
    elif str(open('/sys/firmware/devicetree/base/model').read()) == 'Raspberry Pi Zero W Rev 1.1\x00':
        device = 'RaspberryPiZero'
    else:
        print('Not yet support for this device')
        exit()
except Exception as error:
    print(error)
    exit()

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

try:
    if device == 'OrangePiZero':
         import tsl2591
         tsl2591 = tsl2591.Tsl2591()
except ImportError:
    install('https://github.com/adafruit/Adafruit_Python_MCP9808/archive/master.zip')
    if device == 'OrangePiZero':
         import tsl2591
         tsl2591 = tsl2591.Tsl2591()
    print("Installing lux sensor")
except Exception as error:
    print(error)

try:
    if device == 'OrangePiZero':
        import Adafruit_MCP9808.MCP9808 as MCP9808
        mcp9808 = MCP9808.MCP9808(busnum=0)
        mcp9808.begin()
except ImportError:
    install('https://github.com/maxlklaxl/python-tsl2591/archive/master.zip')
    print("Installed temp sensor")
    if device == 'OrangePiZero':
        import Adafruit_MCP9808.MCP9808 as MCP9808
        mcp9808 = MCP9808.MCP9808(busnum=0)
        mcp9808.begin()
except Exception as error:
    print(error)

try:
    if device == 'RaspberryPiZero':
        import board
        import busio
        import adafruit_si7021
        i2c = busio.I2C(board.SCL, board.SDA)
        si7021 = adafruit_si7021.SI7021(i2c)
except ImportError:
    install('adafruit-circuitpython-si7021')
    print("Installed temp sensor")
    import board
    import busio
    import adafruit_si7021
    i2c = busio.I2C(board.SCL, board.SDA)
    si7021 = adafruit_si7021.SI7021(i2c)
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
        if device == 'OrangePiZero':
            try:
                temp = int(mcp9808.readTempC()*10-16)/10
                return temp, 200
            except Exception as error:
                print(error)
                return "Server error", 500
        elif device == 'RaspberryPiZero':
            try:
                temp = int(si7021.temperature*10)/10
                return temp, 200
            except Exception:
                return "Server error", 500

class humidity(Resource):
    def get(self):
        if device == 'RaspberryPiZero':
            try:
                humidity = int(si7021.relative_humidity*10)/10
                return humidity, 200
            except Exception:
                return "Server error", 500
        else:
            return "does not have this feature", 404

class lux(Resource):
    def get(self):
        if device == 'OrangePiZero':
            try:
                full, ir = tsl2591.get_full_luminosity()
                lux = int(tsl2591.calculate_lux(full, ir)*10)/10
                return lux, 200
            except Exception as error:
                return "Server error", 500
        else:
            return "Does not have this function", 404

@app.errorhandler(404)
def does_not_exist(Resource):
    return "Does not exist\n", 404

api.add_resource(cpu, "/cpu")
api.add_resource(humidity, "/humidity")
api.add_resource(temp, "/temp")
api.add_resource(lux, "/lux")

serve(app, host='0.0.0.0', port=5000)
