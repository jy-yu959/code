import serial #导入serial模块
import zmq
import time
ip="192.168.137.1"
ser = serial.Serial("/dev/ttyAMA0",9600)#打开串口，存放到ser中，/dev/ttyUSB0是端口名，9600是波特率


context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://%s:8899"%ip)
print("OK")
jing="none"
wei="none"


while True:

    line = str(ser.readline())  # readline()是用于读取整行
    times = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    # 这里如果从头取的话，就会出现b‘，所以要从第三个字符进行读取
    if line.startswith("b'$GNGGA"):
        #我这里用的GPGGA，有的是GNGGA
        print(line)
        line = str(line).split(',')  # 将line以“，”为分隔符
        if line[4]!='':

            jing = str(float(line[4][:3]) + float(line[4][3:])/60)
        # 读取第5个字符串信息，从0-2为经度，即经度为116，再加上后面的一串除60将分转化为度
        if line[2]!='':
            wei = str(float(line[2][:2]) + float(line[2][2:])/60)
        temp=jing+"/"+wei

        msg=temp+"/"+times
        msg=msg.encode('utf-8')
        print(msg)

        socket.send(msg)
        response = socket.recv()
        response = str(response, encoding="utf8")
        print(response)