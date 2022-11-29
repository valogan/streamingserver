from socket import *
import threading # for multiple clients
import cv2 # for video
import pickle # serializes data
import struct # convert data to format that can be sent with sockets
import queue
import signal

ADDR = ("", 6789)

def signal_handler(sig, frame, socket):
    print("closing sockets and exiting...")
    socket.close()
    exit(0)

def readVideo(vid, messages, videoStarted, video):
    print("read video thread started")
    video.set()
    while(vid.isOpened()):
        ret, frame = vid.read()
        if not ret:
            print("no more video")
            return
        serialFrame = pickle.dumps(frame)
        message = struct.pack("Q", len(serialFrame)) + serialFrame
        messages.put(message)
        #print(messages.qsize())
        videoStarted.set()
    vid.release()
    video.unset()
    print("returning from read video")
    return
        
def sendVideo(conn, messages, videoStarted, video):
    print("send video thread started")
    #print(messages)
    while not videoStarted:()
    while(video):
        for i in range(messages.qsize()):
            conn.sendall(messages.get())
            #print(messages.qsize())
    print("returning from sendVideo")
    return

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    vid = cv2.VideoCapture(0)
    videoStarted = threading.Event()
    video = threading.Event()
    video.set()
    if(vid.isOpened()):
        messages = queue.Queue()
        readThread = threading.Thread(target = readVideo, args = (vid, messages, videoStarted, video))
        readThread.start()
        sendThread = threading.Thread(target = sendVideo, args= (conn, messages, videoStarted, video))
        sendThread.start()

signal.signal(signal.SIGINT, signal_handler)
            
def main():
    print("Starting server...")
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(ADDR)
    server.listen() # number of connections that can be accepted
    print(f"server is listening on {ADDR}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()

if __name__ == "__main__":
    main()
