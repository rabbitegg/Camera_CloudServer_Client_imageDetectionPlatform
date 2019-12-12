#!/usr/bin/python
# -*-coding:utf-8 -*-
import socket
import cv2
import numpy

# 接受图片大小信息
def rev_size(sock, count):
    buf = ''
    while (count):
        newbuf = sock.rev(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

address = ('10.0.0.30', 8010)
sock_server.bind(address)
sock_server.listen(True)
print('Waiting for images...')


conn, addr = sock_server.accept()
while True:
    length = rev_size(conn, 16)
    if isinstance(length, str):
        stringData = rev_size(conn, int(length))
        data = numpy.fromstring(stringData, dtype='uint8')
        decimg = cv2.imdecode(data, 1)
        cv2.imshow('SERVER', decimg)
        if cv2.waiteKey(10) == 27:
            break
            print('Image received successfully!')
    if cv2.waiteKey(10) == 27:
        break
sock_server.close()
cv2.destroyAllWindows()