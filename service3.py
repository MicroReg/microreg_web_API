from flask import Flask,request

app = Flask(__name__)

@app.route("/auth",methods=["POST"])
def auth():
    a=request.get_data()
    # print dir(request)
    v=request.get_json()
    print a,v
    print "request received"
    return v

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=10002)
