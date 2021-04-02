import socket
import json
import time
import csv
from pprint import pprint
import signal

UDP_IP = "localhost"
UDP_PORT = 10000

class Parser:
    def __init__(self):
        try:
            with open("config.txt","r",encoding="utf-8") as f:
                self.csvPath = f.readline()
                print(self.csvPath)
        except FileNotFoundError as e:
            print("Archivo no existe")
            print(e)
    
    def load_csv(self):
        print("LOADING CSV FILE....")
        data = []
        with open(self.csvPath, newline='') as csvfile:
            spamreader = csv.DictReader(csvfile)
            #print(type(spamreader))
            for row in spamreader:
                #print(row)
                row["value1"] = row.pop("compra")
                row["value2"] = row.pop("venta")
                row["name"] = row.pop("nombre")
                data.append(row)
            #pprint(data)
            self.data_json = json.dumps(data, sort_keys=False, indent=4)
    
    def handler(self, sig, frame):
        print(sig)
        print('CERRANDO socket')
        self.sock.close()
        exit(0)

    def loop(self):
        try:
            signal.signal(signal.SIGINT, self.handler)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            while True:
                self.load_csv()
                print(self.data_json)
                self.sock.sendto(self.data_json.encode("utf-8"), (UDP_IP, UDP_PORT))
                (data, addr) = self.sock.recvfrom(1024)
                print(data)
                time.sleep(30)
        except Exception as e:
            print(e)

p = Parser()
p.loop()