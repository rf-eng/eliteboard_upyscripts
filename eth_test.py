import network
import time
import socket

def http_get(url):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break

lan = network.LAN()
lan.active(True)
while not(lan.isconnected()):
    time.sleep(0.1)

ip_settings = lan.ifconfig()
print("IP: {}".format(ip_settings[0]))
print("netmask: {}".format(ip_settings[1]))
#print(": {}".format(ip_settings[2]))

http_get('http://micropython.org/ks/test.html')