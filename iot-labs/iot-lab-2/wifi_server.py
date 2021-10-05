import socket
import picar_4wd as fc
import time
from threading import Thread
import json

HOST = "192.168.1.89" # IP address of your Raspberry PI
PORT = 65431
power_val = 600
direction = 'stop'

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
                    time.sleep(0.7)
                    fc.forward(power_val)
                    direction = 'forward'
                    print(direction)
                elif direction == 'right' :
                    print(direction)
                    fc.turn_right(power_val)
                    time.sleep(0.7)
                    fc.forward(power_val)
                    direction = 'forward'
                    print(direction)
                elif direction == 'backward' :
                    print(direction)
                    fc.backward(power_val)
                elif direction == 'stop' :
                    print(direction)
                    fc.stop()      
                
        except Exception as e: 
            print("Closing socket")
            print(e)
            #client.close()

if __name__ == '__main__':

    server()
