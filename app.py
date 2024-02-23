from flask import Flask, request

from tools.server import Server

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "hello"


@app.route("/wechat_service", methods=["GET", "POST"])
def wechat_service():
    if request.method == "GET":
        return Server.bind_server(request)
    elif request.method == "POST":
        print("Post")
        return Server.send_message(request)


if __name__ == '__main__':
    app.run(debug=True)
