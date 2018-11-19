from flask import Flask
from flask_script import Manager, Server

app = Flask(__name__)
manager = Manager(app)
manager.add_command("runserver", Server(use_debugger=True))

@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == "__main__":
    manager.run()