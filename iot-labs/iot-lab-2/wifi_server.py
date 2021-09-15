import socket
import picar_4wd as fc
import time
from threading import Thread
import json

HOST = "192.168.1.89" # IP address of your Raspberry PI
PORT = 65432
power_val = 600
direction = 'stop'

class wifi_server(Thread):
    def run(self):
        print('started server')
        global direction
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            
            try:
                while 1:
                    print('rached here')
                    client, clientInfo = s.accept()
                    print("server recv from: ", clientInfo)
                    data = client.recv(1024)      # receive 1024 Bytes of message in binary format
                    if data != b"":
                        direction = data.decode() 
                        client.sendall(data) # Echo back to client
                    if direction == 'forward' :
                        print(direction)
                        fc.forward(power_val)
                    elif direction == 'left' :
                        fc.turn_left(power_val)
                        print(direction)
                        time.sleep(0.3)
                        fc.forward(power_val)
                        direction = 'forward'
                        print(direction)
                    elif direction == 'right' :
                        print(direction)
                        fc.turn_right(power_val)
                        time.sleep(0.3)
                        fc.forward(power_val)
                        direction = 'forward'
                        print(direction)
                    elif direction == 'backward' :
                        print(direction)
                        fc.backward(power_val)    
                    
            except: 
                print("Closing socket")
                client.close()
                s.close()

class move_car(Thread):
    def run(self):
        print('started car')
        global direction
        while 1:
            if direction == 'forward' :
                print(direction)
                fc.forward(power_val)
            elif direction == 'left' :
                #fc.turn_left(power_val)
                print(direction)
                time.sleep(0.)
                direction = 'forward'
                print(direction)
            elif direction == 'right' :
                print(direction)
                fc.turn_right(power_val)
                time.sleep(0.3)
                direction = 'forward'
                print(direction)
            elif direction == 'backward' :
                print(direction)
                #fc.backward(power_val)

def server():
    print('server')
    global direction
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        
        try:
            while 1:
                print('rached here')
                client, clientInfo = s.accept()
                print("server recv from: ", clientInfo)
                data = client.recv(1024)      # receive 1024 Bytes of message in binary format
                if data != b"":
                    direction = data.decode()
                    results = fc.pi_read()
                    results['Status'] = direction
                    if direction == 'left' :
                        results['Status'] = 'Turn left and move forward'
                    if direction == 'right' :
                        results['Status'] = 'Turn right and move forward'
                    #print(json.dumps(results))
                    result = json.dumps(results)
                    client.sendall(result.encode()) # Echo back to client
                if direction == 'forward' :
                    print(direction)
                    fc.forward(power_val)
                elif direction == 'left' :
                    fc.turn_left(power_val)
                    print(direction)
                    time.slee
