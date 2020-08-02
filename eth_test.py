import network
import time

lan = network.LAN()
lan.active(True)
while not(lan.isconnected()):
    time.sleep(0.1)

ip_settings = lan.ifconfig()
print("IP: {}".format(ip_settings[0]))
print("netmask: {}".format(ip_settings[1]))
#print(": {}".format(ip_settings[2]))