from flask import Flask, request
from predict import Models

models = Models()
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
    models.save()

@app.route('/score', methods=['POST'])
def score():
    text = str(request.form['some_string'])
    reversed_string = text[-1::-1]
    return ''' output: {}  '''.format(reversed_string)


if __name__ == '__main__':
    # TODO: unpickle all models and save them to models dictionary
    db.event_model = None # TODO


    app.run(host='0.0.0.0', port=8080, debug=True)
