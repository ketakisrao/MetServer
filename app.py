from flask import Flask
app = Flask("MetServer")

@app.route('/', methods=['GET'])
def default_response():
    return 'Hello, World!'



app.run(threaded=True)