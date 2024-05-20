from flask import Flask

app = Flask(__name__)

# Define your routes and application logic here
@app.route('/')
def hello_world():
    return 'Hello, CardioIB!'

if __name__ == '__main__':
    app.run(debug=True)
