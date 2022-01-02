import os

import zmq
from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler

position = {
    'h': 39.966415999999995,
    'v': 116.36299083333333
}


class LoginHandler(RequestHandler):
    def get(self):
        self.render('login.html')


class IndexHandler(RequestHandler):
    def get(self):
        name = self.get_argument('uname')
        pwd = self.get_argument('pwd')

        if name == 'pi':
            if pwd == '123456':
                self.render('index.html', position=0)
            else:
                self.write('密码错误！')
        else:
            self.write('用户不存在！')

    def post(self):
        data = self.request.body
        data = str(data, 'utf-8')
        data = eval(data)
        # print(data['v'])
        if(data['v']!=''):
            position['v'] = float(data['v']) + 0.0124
            position['h'] = float(data['h']) + 0.007
            print('OK')
        else:
            print('GPS no signal')
        # print(position['v'])


class SocketHandler(WebSocketHandler):
    def open(self, *args: str, **kwargs):
        print('Stand Power!!')

    def on_message(self, message):
        if message == '101010':
            self.write_message('当前位置： 经度： ' + str(position['v']) + '  纬度： ' + str(position['h']))

        elif message == '开始':
            self.write_message('小车已启动')
            print("start")
            socket = zmq.Context().socket(zmq.REQ)
            socket.connect("tcp://192.168.137.85:8899")
            socket.send_string('reflection')

        elif message == '结束':
            self.write_message('小车已停止')
            print("the world!")
            socket = zmq.Context().socket(zmq.REQ)
            socket.connect("tcp://192.168.137.85:8899")
            socket.send_string('blue')

        else:
            self.write_message('error')

    def on_close(self):
        print('xi nei!')

    def check_origin(self, origin: str):
        return True


app = Application([
    (r'^/$', LoginHandler),
    (r'^/index/$', IndexHandler),
    (r'^/WebSocket/$', SocketHandler)
], template_path=os.path.join(os.getcwd(), 'templates'))

app.listen(8848)

IOLoop.instance().start()
