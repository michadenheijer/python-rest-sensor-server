# python-rest-sensor-server
This is my personal project that allows me to access sensors on a Orange Pi Zero using a REST api.

## Sensors
I use the following sensors.
- Adafruit MCP9808
- Adafruit TSL2591
- Orange Pi Zero CPU temp

## Installation
Firstly, clone my project.
```
git clone https://github.com/michadenheijer/python-rest-sensor-server
```

Then make sure you have pip3 and smbus installed.
```
sudo apt install python3-pip, python3-smbus -y
```

Open my project
```
cd python-rest-sensor-server
```

Install dependencies
```
pip3 install -r requirements.txt
```
It might give errors, most often you can ignore those.

Then start the server.
```
python3 api.py
```

Your REST-server is running and you can get information by using:
```
curl http://localhost:5000/cpu
curl http://localhost:5000/temp
curl http://localhost:5000/lux
