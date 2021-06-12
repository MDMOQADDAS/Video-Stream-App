import socket
import cv2
import numpy as np


# Server socket
HOST = '127.0.0.1'
PORT = 50500

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


s.bind((HOST, PORT))


s.listen(10)


# Connection to client socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 1234))

# Accepting Client request
conn, addr = s.accept()


capture = cv2.VideoCapture(0)
model = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


while True:
    # Now caputuing own video 
    ret, own_video = capture.read()
    #Doing decoding
    own_video_decode = cv2.imencode('.jpg', own_video)[1].tostring()
    #Now sending own video|
    sock.sendall(own_video_decode)
    # Data Receive From Other Laptop
    Video_Receive = conn.recv(90456) 
    # Now doing some manupulation
    Video_Receive_in_array = np.fromstring(Video_Receive, np.uint8)
    #Now doing decoding
    Other_laptop_video = cv2.imdecode(Video_Receive_in_array, cv2.IMREAD_COLOR)
    # Showing the video which is come from the other laptop
    cv2.imshow('Linux', Other_laptop_video)
    if cv2.waitKey(10) == 13:
        break
    

cv2.destroyAllWindows()
capture.release()