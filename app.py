from flask import Flask
app = Flask("MetServer")
@app.route('/')
def default_response():
    return 'Hello, World!'