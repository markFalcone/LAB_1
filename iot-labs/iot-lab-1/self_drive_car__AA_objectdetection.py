import sys
import picar_4wd as fc
from picar_4wd.servo import Servo
import time
from datetime import datetime
from picar_4wd.pwm import PWM
from picar_4wd.ultrasonic import Ultrasonic
from picar_4wd.pin import Pin
from picar_4wd.filedb import FileDB
import random
import math
from threading import Thread


from imutils.video import VideoStream
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import cv2

#adding for stop_sign
import picamera
import numpy as np 

from PIL import Image
from tflite_runtime.interpreter import Interpreter
import re,io
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
class HouserBoon(Thread):
    args = {
        "labels": "coco_labels.txt",
        "model": "detect.tflite",
        "threshold": .4
    }

    def load_labels(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            labels = {}
            for row_number, content in enumerate(lines):
                pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
                if len(pair) == 2 and pair[0].strip().isdigit():
                    labels[int(pair[0])] = pair[1].strip()
                else:
                    labels[row_number] = pair[0].strip()
        return labels


    #def __init__(self):
    #    self.labels = self.load_labels(self.args["labels"])
    #    self.interpreter = Interpreter(self.args["model"])
    #    self.interpreter.allocate_tensors()
    #    _, self.input_height, self.input_width, _ = self.interpreter.get_input_details()[0]['shape']

    def set_input_tensor(self, interpreter, image):
        """Sets the input tensor."""
        tensor_index = interpreter.get_input_details()[0]['index']
        input_tensor = interpreter.tensor(tensor_index)()[0]
        input_tensor[:, :] = image


    def get_output_tensor(self, interpreter, index):
        """Returns the output tensor at the given index."""
        output_details = interpreter.get_output_details()[index]
        tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
        return tensor


    def detect_objects(self, interpreter, image, threshold):
        """Returns a list of detection results, each a dictionary of object info."""
        self.set_input_tensor(interpreter, image)
        self.interpreter.invoke()

        # Get all output details
        boxes = self.get_output_tensor(self.interpreter, 0)
        classes = self.get_output_tensor(self.interpreter, 1)
        scores = self.get_output_tensor(self.interpreter, 2)
        count = int(self.get_output_tensor(self.interpreter, 3))

        results = []
        for i in range(count):
            if scores[i] >= threshold:
                result = {
                    'bounding_box': boxes[i],
                    'class_id': classes[i],
                    'score': scores[i]
                }
                results.append(result)
        return results
    
    def run(self):
        ap = argparse.ArgumentParser()
        ap.add_argument("-n", "--num-frames", type=int, default=100,
            help="# of frames to loop over for FPS test")
        ap.add_argument("-d", "--display", type=int, default=-1,
            help="Whether or not frames should be displayed")
        args = vars(ap.parse_args())
        self.labels = self.load_labels(self.args["labels"])
        self.interpreter = Interpreter(self.args["model"])
        self.interpreter.allocate_tensors()
        _, self.input_height, self.input_width, _ = self.interpreter.get_input_details()[0]['shape']
        i = 0
        while True:
            found_stopSign = False
            i = i + 1
            with picamera.PiCamera(resolution=(math.floor(CAMERA_WIDTH), CAMERA_HEIGHT), framerate=30) as camera:
                camera.rotation = 180
                camera.start_preview()
                try:

                    #del results
                    print('reached here')
                    camera.resolution = (320, 240)
                    camera.framerate = 32
                    print("reached here")
                    rawCapture = PiRGBArray(camera, size=(320, 240))
                    stream = io.BytesIO()
                    time1 = datetime.now()
                    camera.capture(stream, format = "jpeg")
                    time2 = datetime.now()
                    abc = time2 - time1
                    print('fps' , 1/abc.total_seconds())
                    fps = FPS().start()
                    
                    image = Image.open(stream).convert('RGB').resize(
                        (self.input_width, self.input_height), Image.ANTIALIAS)
                    print('after error')
                    results = self.detect_objects(self.interpreter, image, self.args["threshold"])
                    for obj in results:
                        print(self.labels[obj['class_id']])
                        if self.labels[obj['class_id']] == "stop sign":
                            print("found stop sign")
                            found_stopSign =  True
                            fc.stop()
                            time.sleep(0.2)

                            fc.forward(70)
                            time.sleep(0.1)
                            
                    stream.seek(0)
                    stream.truncate()
                finally:
                    camera.stop_preview()
            found_stopSign = False
        pass


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

class move_car(Thread):
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

    def scan_angle_in_steps(self,angle,steps):
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

    def scan_step_distance(self):
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

    def run(self):
        while True:
            
            tmp = self.scan_angle_in_steps(90,STEPS)
            #print(tmp)
            status = []
            for d in tmp:
                if d['distance'] <= REF_LENGTH and d ['distance'] > 0:
                   status.append(-1)
                else:
                   status.append(2)
            
            servo = Servo(PWM("P0"),offset=ultrasonic_servo_offset)
            servo.set_angle(0)
            if (status != [2,2,2]):
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
                fc.forward(70)
                print("going straight")
                servo.set_angle(0)
                while True:
                    distance = us.get_distance()
                    #print(distance)
                    if int(distance) < 20 and int(distance) > 0:
                        fc.stop()
                        break

                    #cam = HouserBoon()
                    #print(cam.show_us_the_bolt())

                pass

          

if __name__ == "__main__":
    try:
       fc.forward(50)
       
       cam = HouserBoon()
       print(cam.start())
       time.sleep(0.5)
       mcar = move_car()
       mcar.start()

        #move(15,0)
        #main_falcone()
        #
        #move(29,0)
        #circle_move(90)
    finally:
        fc.stop()


