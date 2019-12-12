import cv2
import socket
import numpy
from time import sleep
import time

# socket.AF_INET     用于服务器与服务器之间网络通信
# socket.SOCKET_STREAM 代表基于TCP的流式socket通信
sock = socket.socket(socket.AF_INET, socket.SOCKET_STREAM)
# connect to Server
address_server = ('192.168.1.2', 8888)
socket.connect(address_server)

# get image from camera
cap = cv2.VideoCapture(0)

# cap.read()      按帧读取视频 
# ret frame是cap.read() 返回值
# ret      布尔值，读帧正确与否
# frame             每一帧图像

ret, frame = cap.read()
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]

while ret:
    # 对图片编码，socket不支持直接发送图片
    img_encode = cv2.imencode('.jpg', frame, encode_param)[1]
    data = numpy.array(img_encode)
    stringData=data.tostring()
    # 先发送图片编码后的长度
    sock.send(str(len(stringData)).ljust(16))
    # 再一字节一字节发送编码的内容
    # 接收端如果为python编程可一次性发送，其他语言需要分开发因为编码中可能会有截断
    """
    for i in range (0, len(stringData)):
        sock.send(stringData[i]) 
    """
    sock.send(stringData)
    ret, frame = cap.read()
    cv2.resize(frame, (640, 480))

sock.close()
cv2.destoryAllWindows()
