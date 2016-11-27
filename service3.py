from flask import Flask,request,session
from micro_reg import MicroRegClient

app = Flask(__name__)

@app.route("/auth",methods=["GET","POST"])
def auth():
    if request.method == "GET":
        return "Send Your Credentials Now"
    else:
        data=request.get_json()
        user = data["username"]
        tok = data["token"]
        if user == "mirage" and tok == "mirage123":
            session["logged_in"]=user
            return "Authentication Succesful"
        else:
            return "Authentication Failed"

@app.route("/auth/check",methods=["GET"])
def check():
    if "logged_in" in session:
        return "Logged in"
    else:
        return "Not Logged in"

if __name__ == '__main__':
    m=MicroRegClient(host="http://192.168.2.215",port=8000)
    m.register("auth_service","http://192.168.2.240",port=10002)
    app.run(debug=True,host="0.0.0.0",port=10002)
