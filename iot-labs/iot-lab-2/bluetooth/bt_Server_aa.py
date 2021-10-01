import bluetooth
import picar_4wd as fc
import json

hostMACAddress = "E4:5F:01:40:45:02" # The address of Raspberry PI Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 0
backlog = 1
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)
print("listening on port ", port)
try:
    client, clientInfo = s.accept()
    while 1:   
        print("server recv from: ", clientInfo)
        data = client.recv(size)
        print(data)
        if data != b"":
            print(data)
            direction = data.decode()
            print(data)
            results = fc.pi_read()
            print(data)
            results['Status'] = direction
            print(direction)
            if direction == 'left' :
                results['Status'] = 'Turn left and move forward'
            if direction == 'right' :
                results['Status'] = 'Turn right and move forward'
            print(json.dumps(results))
            result = json.dumps(results)
            client.sendall(result.encode()) # Echo back to client
        
#if data:
        #    print(data)
        #    client.send(data) # Echo back to client
except: 
    print("Closing socket")
    client.close()
    s.close()


