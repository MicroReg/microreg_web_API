try:
    import  MicroRegClient
except:
    from micro_reg_mod import MicroRegClient

from flask import Flask, request, url_for, render_template, flash, redirect
import json
from cred import username,token
from datetime import datetime
from functools import wraps
from threading import Thread
import time
# from database.MicroDB import MicroDB

#----------Flask instannce--------------!
app = Flask(__name__)

#!!-----authentication session dictionary--------!
auth_dict = {}

#!-----------Global MircroRegClient Instance---------!
microreg = {"inst":None}

#!---------------Universal Json Responses----------!
res={"status":"1"}
err = {"status":"0","message":"Error Occured in the process"}

#!-------------Login Authenticators Decorator---------------!
def login_required(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        # global auth
        if "username" in auth_dict:
            # print "USER LOGGED IN"
            return f()
        else:
            return "USER NOT LOGGED IN"
    return wrap

def time_diff(start,end):
    diff = end-start
    tot = diff.total_seconds()
    if tot >= 1800:
        return True
    else :
        return False

def timeout():
    while(1):
        time.sleep(2)
        # print "Thread running at: ",datetime.now().strftime("%H:%M:%S")
        global auth_dict
        try:
            # print auth_dict['timestamp']
            s = auth_dict['timestamp']
            e = datetime.now()
            r = time_diff(s,e)
            # print "response",r
            if r == False:
                pass
            else:
                auth_dict = {}
                print "session cleared"
        except KeyError as e:
            pass


#!---------------Routing APIs-----------------------!
@app.route("/authentication",methods=["POST"])
def auth():
    # print request.args
    # user=request.args["username"]
    # tok=request.args["token"]
    data = request.get_json()
    user = data["username"]
    tok = data["token"]
    if (user == username) or (tok == token):
        global auth_dict
        auth_dict["username"] = user
        auth_dict["token"] = token
        auth_dict["timestamp"] = datetime.now()
        # return json.dumps({"status":1}) #success
        return json.dumps({"status":[1]})
    else:
        # return json.dumps({"status":0}) #failure
        return json.dumps({"status":[0]})

@app.route("/",methods=["GET"])
@login_required
def home():
    global microreg
    data=request.get_json()
    print data
    host = "http://"+str(data['host'])
    port = int(data['port'])
    try:
        microreg["inst"]=MicroRegClient(host,port)
        return json.dumps({"status":"1","message":" MicroRegClient Initiated" })
    except:
        return json.dumps({"status":"0","message":"Error Occured in  MicroRegClient Instantiation"})

@app.route("/get_all_service_details",methods=["GET"])
@login_required
def get_all_service_details():
    global microreg
    try:
        return  microreg["inst"].get_all_service_details()
    except:
        return json.dumps(err)

@app.route("/get_reg_count",methods=["GET"])
@login_required
def get_reg_count():
    global microreg
    try:
        return json.dumps({"status":"1","data":str( microreg["inst"].get_reg_count())})
    except:
        return json.dumps(err)

@app.route("/get_service_details",methods=["GET"])
@login_required
def get_service_details():
    global microreg
    data = request.get_json()
    try:
        name = data['name']
    except KeyError:
        return json.dumps(err)
    try:
        return json.dumps({"status":"1","data":str( microreg["inst"].get_service_details(name))})
    except:
        return json.dumps(err)


@app.route("/unregister",methods=["GET"])
@login_required
def unregister():
    global microreg
    data = request.get_json()
    # print "<<<<<<<<<<<<<<<<<data>>>>>>",data
    try:
        name = data['name']
    except KeyError:
        return json.dumps(err)
    try:
        return json.dumps({"status":"1","data":str( microreg["inst"].unregister(name))})
    except :
        return json.dumps(err)

@app.route("/login_page",methods=["GET"])
def front():
    return render_template("login.html")

@app.route("/landing_page",methods=["POST"])
def land():
    print request.method
    data = request.form
    print data
    user = data["username"]
    pswd = data["password"]
    if user == username and pswd == token :
        return render_template("index.html")
    else:
        flash("Incorrect Username or Password")

if __name__ == '__main__':
    t1=Thread(target=timeout)
    t1.start()
    # timeout()
    app.run(debug=True,host="0.0.0.0",port=10001)
