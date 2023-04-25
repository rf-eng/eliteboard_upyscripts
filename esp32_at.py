import machine
import uselect
import time

class ESP32_AT:
    def __init__(self, uart):
        self.uart = uart
        self.uart.init(baudrate=115200, timeout=1000, rxbuf=2048)
        self.poll = uselect.poll()
        self.poll.register(self.uart, uselect.POLLIN)
    
    def __del__(self):
        uart.deinit()
        
    def run_cmd(self, string, timeout):
    #     print('run cmd')
        self.uart.write(string)
        time.sleep_ms(10)
        done = False
        res = ''    
        eventlist = self.poll.poll(timeout)
        while (len(eventlist)>0) and not(done):
            res_tmp = self.uart.read(1)
            res += res_tmp.decode('ascii', 'ignore')
            if ('OK\r\n' in res) or ('ERROR\r\n' in res):
                # print('done')
                done = True
            if not(done):
                eventlist = self.poll.poll(timeout)
        if len(eventlist)==0:
            print('timeout')
        return res
    #     print('final result')
    #     print(res+'\n')
    #     print('exit cmd fct.')

    def proc_scan_res(self, string):
        result = list()
        lines = string.split('\r\n')
        for line in lines:
            if line.startswith('+CWLAP'):
                tmp = line.split(',')
                ssid = tmp[1].strip('"')
                rssi = int(tmp[2])
                mac = tmp[3].strip('"')
                result.append({'ssid': ssid, 'rssi': rssi, 'mac': mac})
        return result
