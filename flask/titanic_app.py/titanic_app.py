from flask import Flask
app = Flask(__name__)

#-------- MODEL GOES HERE -----------#

#-------- ROUTES GO HERE -----------#

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = '4000'

    app.run(HOST, PORT)
