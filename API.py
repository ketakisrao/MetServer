from flask import Flask
app = Flask("MetServer")
@app.route('/')
def hello_world():
    return 'Hello, World!'