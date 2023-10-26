import os
import socket
import tqdm
from Crypto.Cipher import AES

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 32768

key = b"iamonlyonesonali"
nonce = b"iamonlytwosonali"

cipher = AES.new(key, AES.MODE_EAX, nonce)


def createSocket():
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sender_socket


def connectWithReceiver(receiver_ip, receiver_port, sender_socket):
    try:
        sender_socket.connect((receiver_ip, receiver_port))
        print("Connected with the receiver at", receiver_ip+":"+receiver_port+" ...")
    except:
        print("Error connecting with the receiver!")


# file_name=input("Enter the file name (with extension): ")
# file_size = os.path.getsize(file_name)


def sendFile(file_to_send, file_name, file_size, sender_socket):

    print("Sending file details: ", file_name, file_size)
    
    sender_socket.send(f"{file_name}{SEPARATOR}{file_size}".encode())
    progress = tqdm.tqdm(
        range(file_size),
        f"Sending {file_name}",
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    )

    with open(file_name, "rb") as f:
    # try:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            encrypted = cipher.encrypt(bytes_read)
            sender_socket.sendall(encrypted)
            progress.update(len(bytes_read))
    # finally:
    #     file_to_send.close()

def closeSocket(sender_socket):
    sender_socket.close()
