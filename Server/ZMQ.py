import zmq
import requests
import json

status = 'stop'

if __name__ == '__main__':
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://192.168.137.85:8899")
    while True:
        message = socket.recv()
        m = str(message, encoding="utf8")
        print(m)
        if m == 'blue':
            print('停车')
            status = 'stop'
            socket.send_string(status)
        elif m == 'reflection':
            print('启动')
            status = 'start'
            socket.send_string(status)
        else:
            data = m.split('/')
            print(data)
            file = open('./data/position.txt', mode='w+')
            file.write(m)
            file.close()
            res = requests.post(url="http://192.168.137.85:8848/index/", data=json.dumps({"v": data[0], "h": data[1]}))
            socket.send_string(status)
        if m == 'q':
            print("client exit")
