import socket
import json
import os
import sys

class Moneda:
    def __init__(self,id,name,value1,value2):
        self.id=id
        self.name = name
        self.value1 = value1
        self.value2 = value2


class Model:
    def __init__(self):
        self.prices = []


    def updateData(self,data):
        print("update data")
        self.prices = []
        for o in data:
            self.prices.append(Moneda(o["id"],o["name"],o["value1"],o["value2"]))



class View:

    def __init__(self,model):
        self.model = model

    def show(self):
        os.system('clear')
        print("MONEDA\t\tCOMPRA\t\tVENTA")
        for m in self.model.prices:
            print(m.name+":\t\t"+str(m.value1)+"\t\t"+str(m.value2))

class Parser:

    @staticmethod
    def parseData(data):
        return json.loads(str(data,"utf-8"))
       

class Main:

    def __init__(self):
        pass

    def main(self):

        port = 10000
        try:
            port = int(sys.argv[1])
        except:
            print("Puerto incorrecto")
            exit(1)

        self.model = Model()
        self.view = View(self.model)
        

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("localhost", port))
        print("Escuchando puerto "+str(port)+"...")
        while True:
            (data, addr) = s.recvfrom(128*1024)
            data = Parser.parseData(data)
            self.model.updateData(data)
            self.view.show()
            s.sendto(bytearray("OK","utf-8"),addr)

m = Main()
m.main()