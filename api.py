from flask import Flask, jsonify, request, Response, session
from flask_cors import CORS, cross_origin
from core import Core
from class_core import Core_Test
#from class_imaging import Imaging_Test
import json
import io
import os
import csv
import datetime
from Naked.toolshed.shell import execute_js

app = Flask(__name__)
CORS(app)

@app.route("/api/discovery", methods=['GET'])
def discovery():
    execute_js('discovery.js')
    try:
        with open('./devices.json') as json_file:
            data = json.load(json_file)
    except IOError: # parent of IOError, OSError *and* WindowsError where available
        data = 'Devices List haven\'t been loaded yet'
    return jsonify(data)


@app.route("/api/init", methods=['GET', 'POST'])
def init():
    if request.method == 'POST':
        print('Data recieved')
        print(request.data)
        return 'RECIEVED'

@app.route("/api/core_test/<method_name>", methods=['GET'])
def core_test(method_name):
    if request.method == 'GET':
        ip = request.args.get('ip')
        port = int(request.args.get('port'))
        try:
            cam = Core_Test(ip, port, 'admin', 'Supervisor')
        except:
            return jsonify(error = "ONVIFError, " + method_name + " method does not respond. You may check VPN Connection")
        try:
            method = getattr(cam, method_name)
            conformity,response = method()
            response = str(response)
            # response = json.loads(response.replace('\n', '\\n'))
            return jsonify(conformity = conformity, response = response)
        except AttributeError:
            return jsonify(error = "Sorry, " + method_name + " method doesn't exist")
        except:
            return jsonify(error = "ONVIFError, " + method_name + " method does not respond. You may check VPN Connection")

@app.route("/api/imaging_test/<method_name>", methods=['GET'])
def imaging_test(method_name):
    if request.method == 'GET':
        ip = request.args.get('ip')
        port = int(request.args.get('port'))
        try:
            cam = Imaging_Test(ip, port, 'admin', 'Supervisor')
        except:
            return jsonify(error = "ONVIFError, " + method_name + " method does not respond. You may check VPN Connection")
        try:
            method = getattr(cam, method_name)
            conformity = method()
            return jsonify(conformity = conformity)
        except AttributeError:
            return jsonify(error = "Sorry, " + method_name + " method doesn't exist")
        except:
            return jsonify(error = "ONVIFError, " + method_name + " method does not respond. You may check VPN Connection")

@app.route("/api/core_test/load", methods=['GET'])
def core_load():
    try:
        with open('./tests/core.json', 'r') as f:
            data = json.load(f)
    except IOError: # parent of IOError, OSError *and* WindowsError where available
        data = 'Error. Core Test can not be loaded.'
    return jsonify(data)

@app.route("/api/deviceinfo", methods=['GET'])
@cross_origin(origin='*')
def deviceinfo():
    if request.method == 'GET':
        ip = request.args.get('ip')
        port = int(request.args.get('port'))
        cam = Core(ip, port, 'admin', 'Supervisor')
        response = cam.GetDeviceInformation()
        print(response)
        return jsonify(
            IP = ip,
            Port = port,
            Uri = cam.GetSnapshotUri(),
            Manufacturer = response[0],
            Model = response[1],
            FirmwareVersion = response[2],
            SerialNumber = response[3],
            HardwareId = response[4])

@app.route("/api/writecsv", methods=['GET'])
def writecsv():
    if request.method == 'GET':
        ip = request.args.get('ip')
        port = int(request.args.get('port'))
        cam = Core_Test(ip, port, 'admin', 'Supervisor')
        date = str(datetime.datetime.now())
        date = date.split('.')
        header = [['Device IP', ip], ['Test Performed', date[0]]]
        summary = [['Services', cam.DeviceCapabilities()]]
        reportn = os.getcwd() + '/reports/' + ip + '.csv'
        with open(reportn, 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(header)
            writer.writerows(summary)
            writer.writerows([['GetCapabilities', cam.GetCapabilities()], ['GetDiscoveryMode', cam.GetDiscoveryMode()], ['SetDiscoveryMode', cam.SetDiscoveryMode()], ['GetScopes', cam.GetScopes()], ['AddScopes', cam.AddScopes()], ['RemoveScopes', cam.RemoveScopes()], ['GetHostname', cam.GetHostname()], ['SetHostname', cam.SetHostname()], ['GetNetworkInterfaces', cam.GetNetworkInterfaces()], ['GetDNS', cam.GetDNS()], ['GetNetworkProtocols', cam.GetNetworkProtocols()], ['GetNetworkDefaultGateway', cam.GetNetworkDefaultGateway()], ['SetNetworkDefaultGateway', cam.SetNetworkDefaultGateway()], ['GetDeviceInformation', cam.GetDeviceInformation()], ['GetUsers', cam.GetUsers()], ['DeleteUsers', cam.DeleteUsers()], ['GetNTP', cam.GetNTP()], ['GetServices', cam.GetServices()], ['GetSystemDateAndTime', cam.GetSystemDateAndTime()], ['GetSystemUris', cam.GetSystemUris()]])
        csvFile.close()
        return "POSTED_CSV"

@app.route("/api/snapshoturi", methods=['GET', 'POST'])
def snapshoturi():
    #if request.method == 'POST':
        #print('Data recieved')
        #print(request.get_json())
        #return 'RECIEVED'
    if request.method == 'GET':
        ip = request.args.get('ip')
        port = int(request.args.get('port'))
        cam = Core(ip, port, 'admin', 'Supervisor')
        return jsonify(Uri = cam.GetSnapshotUri())

if __name__ == '__main__':
    app.run(debug=True)