import picar_4wd as fc
import random
import time

speed = 30

def back25():
    fc.backward(100)
    x = 0
    for i in range(1):
        time.sleep(0.1)
        x += speed * 0.1
    fc.stop()

def main():
    i = 0
    while i < 40:
        scan_list = fc.scan_step(35)
        if not scan_list:
            continue

        tmp = scan_list[3:7]
        print(tmp)
        if tmp != [2,2,2,2]:
            rand = random.randint(0,1)
            if rand == 0:
                back25()
                fc.turn_left(speed)
            else:
                back25()
                fc.turn_right(speed)
        else:
            fc.forward(speed)
        i = i + 1
    fc.stop()

if __name__ == "__main__":
    try:
        main()
    finally:
        fc.stop()
