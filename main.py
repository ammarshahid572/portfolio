import json
from werkzeug.utils import secure_filename
from flask import Flask, redirect, request, send_file
import requests

from db.deviceDb import get_all_collections, getOta, insertOtaBins, list_all_documents, update_or_insert_doc

app = Flask(__name__, static_folder='assets')

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/display')
def displayControl():
    return send_file('display.html')

@app.route('/map-points')
def maps():
    return send_file('map.html')

@app.route('/favicon.ico')
def favicon():
    return send_file('favicon.ico')

@app.route('/otaupload', methods=['GET', 'POST'])
def uploadOta():
    if request.method=='GET':
        return send_file('otaupload.html')
    else:
        file = request.files['file']
        if '.bin' in file.filename:
            vName= request.form['vName']
            vNumber= request.form['vNumber']
            vClass= request.form['vClass']
            print(vClass,vName)
            filename = f'{vClass}_{vName}.bin'
            insertOtaBins(vClass,vName,vNumber, filename)
            file.save('./bins/'+filename)
            return "success",200
        else:
            return "invalid file type only .bin accepted", 400

@app.route('/getOta/<vClass>', methods=['GET'])
def getOtaInfo(vClass):
    if vClass!='all':
        return getOta(vClass=vClass)
    else:
        return getOta(vClass=None)

@app.route('/bins/<filename>', methods=['GET'])
def downloadBin(filename):
    print(filename)
    return send_file(f'bins/{filename}')

@app.route('/device/data/<collection>', methods=['POST','GET'])
def data(collection):
    if request.method=="POST":
        id=request.headers.get('x-chip-id')
        try:
            sensors=request.json['sensors']
        except Exception:
            sensors=None
        try:
            actuators=request.json['actuators']
        except Exception:
            actuators=None
        update_or_insert_doc(collection,id, sensors=sensors, actuators=actuators)
        return 'Success!', 200
    else:
        id=request.headers.get('x-chip-id')
        if id:
            return list_all_documents(collection, id=id)
        else:
            return list_all_documents(collection, id=None)

@app.route('/device/data/', methods=['GET'])
def getData():
    collections=get_all_collections()
    return collections


@app.route('/downloadResume' , methods=['GET'])
def getResume():
    return redirect('./assets/pdf/Resume-AmmarShahid.pdf')


@app.route('/updateLogs', methods=['POST'])
def updateFile():
    data=request.json
    with open('gpsLogs.txt', 'a') as f:
        f.write('\n')
        f.write(json.dumps(data))
    return 'success',200
@app.route('/sendMessage', methods=['POST','GET'])
def sendMessage():
    if request.method=='POST':
        data= request.json
        print(data)
        message= "Name: "+data['name']+"\nEmail: "+data['email']+" \nMessage: "+data["message"]
        
        # set up the webhook URL and message payload
        webhook_url = "https://discordapp.com/api/webhooks/1082215154810368020/L8MZ8Gafqyk9pmjIGO1v8IQIeQ6jjiD7keup-cPT3RQk_EcU5q3lck3-tXUm61yoTswN"
        payload = {
            "content": message
        }
        headers = {
            "Content-Type": "application/json"
        }
        
        requests.post(webhook_url, data=json.dumps(payload), headers=headers)

        return json.dumps({'data':"success"})
    else:
        return "get sucess", 200 
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000) # Change the port to 5000