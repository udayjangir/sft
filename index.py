from flask import Flask, render_template, request, redirect
import os
import sender
import receiver
import socket
import threading
from pymongo import MongoClient

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["RECEIVED_FOLDER"] = "received"
app.config["STATIC_FOLDER"] = "static"
app.config["MONGO_URI"] = "mongodb://localhost:27017/ekthadb"

app.config["RECEIVER_PORT"] = 9999

mongo = MongoClient(app.config["MONGO_URI"])
db = mongo.get_database()

def startReceive():
    receiver_socket = receiver.bindSocket()
    print("Started receiving ...")
    receiver.startReceiving(receiver_socket)

thread = threading.Thread(target=startReceive)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/send", methods=["POST"])
def sendFile():
    RECEIVER_IP = request.form.get("receiver_ip")

    if "file" not in request.files:
        return "No file part"

    file = request.files["file"]

    if file.filename == "":
        return "No selected file"

    if file:
        filename = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filename)
        file_name = os.path.abspath(filename)
        print("File name is: ", file.filename)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        sender_socket = sender.createSocket()
        sender.connectWithReceiver(
            receiver_ip=RECEIVER_IP,
            receiver_port=app.config["RECEIVER_PORT"],
            sender_socket=sender_socket,
        )
        sender.sendFile(
            file, file_name=file_name, file_size=file_size, sender_socket=sender_socket
        )
        sender.closeSocket(sender_socket)
        return "File successfully sent"


@app.route("/send_page", methods=["GET"])
def goToSendPage():
    return render_template("send_page.html")


@app.route("/receive_page", methods=["GET", "POST"])
def goToReceivePage():
    receiving_state = request.args.get("state")
    print(receiving_state)
    if (request.method == "GET") and receiving_state == "offline":
        active_users = db.active_users
        user_ip = socket.gethostbyname(socket.gethostname())
        current_user = active_users.delete_many({"userIp": user_ip})
        receiver.closeSocket()
        return render_template("receive_page.html", isOnline=False, value=None)

    elif request.method == "GET":
        return render_template("receive_page.html", isOnline=False, value=None)

    elif request.method == "POST" and receiving_state == "online":
        active_users = db.active_users
        user_name = request.form.get("userName")
        user_ip = socket.gethostbyname(socket.gethostname())

        active_users.insert_one({"userName": user_name, "userIp": user_ip})

        current_user = active_users.find_one(
            {"userIp": socket.gethostbyname(socket.gethostname())}
        )

        thread.start()

        return render_template("receive_page.html", isOnline=True, value=current_user)


@app.route("/registerUser", methods=["POST"])
def registerUser():
    users = db.users
    user_name = request.form.get("userName")
    user_ip = socket.gethostbyname(socket.gethostname())
    users.insert_one({"userName": user_name, "userIp": user_ip})
    return "User registered"


if __name__ == "__main__":
    app.run(debug=True)
