from crypt import methods
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')

@app.route('/getData',methods=['POST'])
def getData():
    return "Loading the Data ..."

if __name__ == '__main__':
    app.run(debug=True)
