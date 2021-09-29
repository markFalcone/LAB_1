import bluetooth

#hostMACAddress = "DC:A6:32:80:7D:87" # The address of Raspberry PI Bluetooth 
hostMACAddress = "E4:5F:01:40:57:A3" # replace with our own Pi MAC
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
        if data:
            print(data)
            client.send(data) # Echo back to client
