from flask import  Flask,jsonify,request
from main import *

app = Flask(__name__)

@app.route('/')
def main():
    go()
    return jsonify({"message": "pong!"})


if __name__=='__main__':
    app.run(host='0.0.0.0', port=80)
