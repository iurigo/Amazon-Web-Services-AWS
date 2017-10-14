from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello Turings"

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = '4000'

    app.run(HOST, PORT)
