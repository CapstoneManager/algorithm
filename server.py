from flask import Flask, request
import MinCostMaxFlow
import threading
import requests

app = Flask(__name__)

running = False

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/algorithm', methods=['POST'])
def algorithm():
    print("running /algorithm")
    global running
    if (running == False):
        data = request.get_json()
        threading.Thread(target=process(data)).start()
    return ""

@app.route('/status', methods=['GET'])
def checkStatus():
    if (running == False):
        return "false"
    else:
        return "true"

def process(data):
    global running
    running = True
    result = MinCostMaxFlow.flow(data["students"], data["projects"], data["projMinCapacity"], data["projMaxCapacity"], data["rankings"])
    r = requests.post('http://localhost:8443/assign-to-students', json=result)
    running = False
