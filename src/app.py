from predict import Logic
from EventAPIClient import EventAPIClient
import threading
from flask import Flask, request, render_template, session, redirect

app = Flask(__name__)

# @app.route('/', methods=['GET'])
# def home():
#     return ''' <h2> Triage Dashboard </h2>
#                    <a href="/hello">hello</a> and an
#                    <a href="/save">Save user data before stopping the app</a> </p> '''


@app.route('/', methods=("POST", "GET"))
def html_table():
    df = logic.db.event_df[['previous_payouts', 'email_domain', 'payout_type']]
    return render_template('index.html',
                           tables=[df.to_html(classes='blueth')],
                           titles=['na','New events'])


@app.route('/hello', methods=['GET'])
def hello_world():
    return ''' <h1> Hello, World!</h1> '''

if __name__ == '__main__':
    # TODO: unpickle all models and save them to models dictionary
    logic = Logic()
    event_api = EventAPIClient(logic=logic)

    t = threading.Thread(target=event_api.collect)
    t.start()
    app.run(host='0.0.0.0', port=8080, debug=True)
