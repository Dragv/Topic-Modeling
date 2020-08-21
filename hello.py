
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/send', methods=['POST'])
def hello_world():
    request.form('text')
    return 'Hello, World!'



app.run()