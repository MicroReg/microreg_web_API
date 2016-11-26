try:
    import MicroRegClient
except:
    import os
    print os.getcwd()
    from micro_reg import MicroRegClient

from flask import Flask, request
import json

app = Flask(__name__)

microreg = None

res={"status":"1"}
err = {"status":"0","message":"Error Occured in the process"}

@app.route("/",methods=["GET"])
def home():

    '''json request example
        {"host":"<name of host>","port":"<port number>"}
    '''

    global microreg
    data=json.loads(request.get_json())
    host = data['host']
    port = data['port']
    try:
        microreg = MicroRegClient(host,port)
        return json.dumps({"status":"1","message":"MicroRegClient Initiated"})
    except:
        return json.dumps({"status":"0","message":"Error Occured in MicroRegClient Instantiation"})

@app.route("/get_all_service_details",methods=["GET"])
def get_all_service_details():
    global microreg
    try:
        return json.dumps({"status":"1","data":str(microreg.get_all_service_details())})
    except:
        return json.dumps(err)

@app.route("/get_reg_count",methods=["GET"])
def get_reg_count():
    global microreg
    try:
        return json.dumps({"status":"1","data":str(microreg.get_reg_count())})
    except:
        return json.dumps(err)

@app.route("/get_service_details",methods=["GET"])
def get_service_details():

    '''
        json example
        {"name":"<name of the service whose details are required>"}
    '''

    global microreg
    data = request.get_json()
    name = data['name']
    try:
        return json.dumps({"status":"1","data":str(microreg.get_service_details(name))})
    except:
        return json.dumps(err)


@app.route("/unregister",methods=["GET"])
def unregister():

    '''
        json example
        {"name":"<name of the service to be terminated>"}
    '''

    global microreg
    data = request.get_json()
    name = data['name']
    try:
        return json.dumps({"status":"1","data":str(microreg.unregister(name))})
    except:
        return json.dumps(err)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=10001)
