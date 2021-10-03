import bluetooth
import picar_4wd as fc
import json

hostMACAddress = "E4:5F:01:40:57:A3" # The address of Raspberry PI Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
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
        print('Receive direction from the client: ', data)
        if data != b"":
            direction = data.decode()
            results = fc.pi_read()
            print('Pi car parameters before executing the direction from the client: ', results)
            
            if direction == 'left' :
                results['Status'] = 'Turn left and move forward'
            if direction == 'right' :
                results['Status'] = 'Turn right and move forward'
            if direction == 'forward' :
                results['Status'] = 'Move forward'
            if direction == 'backward':
                results['Status'] = 'Move backward'
            print('Pi car parameters after executing the direction from the client: ', results)
            
            result = json.dumps(results)
            client.sendall(result.encode()) # Echo back to client
                    
#if data:
        #    print(data)
        #    client.send(data) # Echo back to client
except: 
    print("Closing socket")
    client.close()
    s.close()
