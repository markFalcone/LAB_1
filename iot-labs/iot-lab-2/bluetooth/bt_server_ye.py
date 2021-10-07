import bluetooth
import picar_4wd as fc
import json
import time

SPEED = 25

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
            direction = data.decode().lower()
            print('The direction Pi car received from the client: ', direction)

            if direction == "forward":
                fc.forward(SPEED)
                distance = 0
                for i in range(5):
                    time.sleep(0.1)
                    distance += SPEED * 0.1
            if direction == "backward":
                fc.backward(SPEED)
                distance = 0
                for i in range(5):
                    time.sleep(0.1)
                    distance += SPEED * 0.1

            if direction == "left":
                fc.turn_left(50)
                for i in range(10):
                    time.sleep(0.1)
                fc.forward(SPEED)
                distance = 0
                for i in range(5):
                    time.sleep(0.1)
                    distance += SPEED * 0.1

            if direction == "right":
                fc.turn_right(50)
                for i in range(10):
                    time.sleep(0.1)

                fc.forward(SPEED)
                distance = 0
                for i in range(5):
                    time.sleep(0.1)
                    distance += SPEED * 0.1

            fc.stop()

            # Read stats of pi car and add the distance and speed to the parameter list
            stats = fc.pi_read()
            stats["Direction"] = direction
            stats["Travel_Distance"] = distance
            stats["Car_Speed"] = SPEED
            print('Pi car stats after executing the direction from the client: ', stats)

            stats = json.dumps(stats)
            client.sendall(stats.encode()) # Echo back to client

#if data:
        #    print(data)
        #    client.send(data) # Echo back to client
except:
    print("Closing socket")
    client.close()
    s.close()
