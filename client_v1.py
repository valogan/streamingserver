#importing libraries
from socket import *
import cv2
import pickle
import struct
import imutils
import sys


def main():
    ADDR = (sys.argv[1], int(sys.argv[2]))
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(ADDR)

    data = b""
    payload_size = struct.calcsize("Q") # 8 bytes

    while True:
        while len(data) < payload_size:
            packet = client.recv(1024*1024)
            if not packet: break
            data+=packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]
        while len(data) < msg_size:
            data += client.recv(1024*1024)
        frame_data = data[:msg_size]
        data  = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("Receiving...",frame)
        if cv2.waitKey(16) == 13:
            break
    client.close()



if __name__ == "__main__":
    main()
