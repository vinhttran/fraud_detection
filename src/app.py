from flask import Flask, request
from predict import Logic

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return ''' <h2> Triage Dashboard </h2>
                   <a href="/hello">hello</a> and an 
                   <a href="/save">Save user data before stopping the app</a> </p> '''

@app.route('/hello', methods=['GET'])
def hello_world():
    return ''' <h1> Hello, World!</h1> '''

@app.route('/save', methods=['GET'])
def save():
    logic.save()

@app.route('/score', methods=['POST'])
def score():
    logic.predict(request) # no idea
    # TODO figure out the data we get
    text = str(request.form['some_string'])


if __name__ == '__main__':
    # TODO: unpickle all models and save them to models dictionary
    logic = Logic()
    app.run(host='0.0.0.0', port=8080, debug=True)
