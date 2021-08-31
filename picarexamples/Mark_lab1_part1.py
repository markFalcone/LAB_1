import picar_4wd as fc
import time, math
import sys
import tty
import random
 

key = 'status'
speed = 30

def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)


def goBack():
    
    # time.sleep(2)
    fc.backward(10)
    x = 0
    for i in range(5):
        time.sleep(0.1)
        x += speed * 0.1

def main():
                         
    while True:
        scan_list = fc.scan_step(35)
        if not scan_list:
            continue

        tmp = scan_list[3:7]
        print(tmp)
        if  1 in tmp:
            print("obstical")
            x = random.randint(0, 1)
            if x== 0:
                print('right')
                fc.stop()
#                 for i in range(5):
#                     time.sleep(0.1)
#                     x += speed * 0.1
                goBack()
                fc.turn_right(speed)
                
            else:
                print('left')
                fc.stop()
                goBack()
                fc.turn_left(speed)
        else:
            fc.forward(speed)

if __name__ == "__main__":
    try: 
        main()
    finally: 
        fc.stop()





