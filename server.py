from flask import Flask, request
import MinCostMaxFlow
import threading

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/algorithm', methods=['POST'])
def algorithm():
    data = request.get_json();
    threading.Thread(target=process(data)).start()
    return "";

def process(data):
    MinCostMaxFlow.flow(data["students"], data["projects"], data["projMinCapacity"], data["projMaxCapacity"], data["ranking"])
