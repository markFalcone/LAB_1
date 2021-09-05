
import sys
import picar_4wd as fc
from picar_4wd.servo import Servo
import time
from picar_4wd.pwm import PWM
from picar_4wd.ultrasonic import Ultrasonic
from picar_4wd.pin import Pin
from picar_4wd.filedb import FileDB
import random


speed = 150

REF_LENGTH = 30
angle = 90
config = FileDB()
STEPS = 4
us = Ultrasonic(Pin('D8'), Pin('D9'))
ultrasonic_servo_offset = int(config.get('ultrasonic_servo_offset', default_value = 0))  
servo = Servo(PWM("P0"), offset=ultrasonic_servo_offset)

distance_in_second = 29
time_required_1_CM = 1/distance_in_second


def circle_move(turn_degree):
    fc.turn_left(1000)
    time.sleep(3)

def move(distance_to_move,forward):
    time_required_distance_to_move = time_required_1_CM * distance_to_move
    
    if forward == 1:
        fc.forward(500)
    else:
        fc.backward(500)    
    time.sleep(time_required_distance_to_move)

def scan_angle_in_steps(angle,steps):
    startAngle = int(angle/2)
    endAngle = -int(angle/2)
    step=int(180/steps)*(-1)
    results = []
    for angle in range(45,-46,-45):
        d=fc.get_distance_at(angle)
        item ={}
        item["distance"] = d
        item["angle"] = angle
        results.append(item)
    return results

def scan_step_distance():
    results = []
    for angle in range(90,-91,-5):
        d=fc.get_distance_at(angle)
        item = {}
        if d == -2 :
            d = 120
        item["distance"] = d
        item["angle"] = angle
        results.append(item)
    return results

def main():
    while True:
        tmp = scan_angle_in_steps(90,STEPS)
        print(tmp)
        status = []
        for d in tmp:
            if d['distance'] <= REF_LENGTH and d ['distance'] > 0:
               status.append(-1)
            else:
               status.append(2)
        servo = Servo(PWM("P0"),offset=ultrasonic_servo_offset)
        servo.set_angle(0)
        if status != [2,2,2]:
            servo.set_angle(0)
            #distance = scan_step_distance()            
            #high_distance = {'distance': 0, 'angle': 0}
            #for d in distance:
            #    length = d['distance']
            #    if length >= high_distance['distance'] :
            #        high_distance = d
            #print(high_distance)
            #angle=d['angle']
            #print(angle)
            #if angle < 0:
            fc.turn_left(550)
            #else:
            #    fc.turn_right(600)
            time.sleep(0.63)                 
        else:
            fc.forward(200)
            print("going straight")
            servo.set_angle(0)
            while True:
                distance = us.get_distance()
                if int(distance) < 20 :
                    fc.stop()
                   
                    break
            pass

          

if __name__ == "__main__":
    try:      
       main()
        #move(15,0)
        #main_falcone()
        #
        #move(29,0)
        #circle_move(90)
    finally:
        fc.stop()



