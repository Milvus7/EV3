#!/usr/bin/env python3

from time import sleep
from colorsys import rgb_to_hls

import cube

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_D, MediumMotor # type: ignore
from ev3dev2.sensor import INPUT_1 # type: ignore
from ev3dev2.sensor.lego import ColorSensor # type: ignore
from ev3dev2.led import Leds # type: ignore
from ev3dev2.button import Button # type: ignore

import os

os.system('setfont Lat15-TerminusBold14')
            
class Colors: 
    WHITE = 0
    RED = 1
    BLUE = 2
    YELLOW = 3
    ORANGE = 4
    GREEN = 5
    
    to_string = {
        0: "white",
        1: "red",
        2: "blue",
        3: "yellow",
        4: "orange",
        5: "green"
    }

CORNER_ROTATOR_SCAN_ANGLE = 24.66
EDGE_ROTATOR_SCAN_ANGLE = 75.66

class Bot():
    def __init__(self):
        self.on_cube = False
        
        self.color_sensor = ColorSensor(INPUT_1)
        self.flipper_motor = LargeMotor(OUTPUT_A)
        self.color_sensor_motor = MediumMotor(OUTPUT_B)
        self.rotator_motor = LargeMotor(OUTPUT_D)
        
        #if the ev3 is not rebooted between each program run, this is needed for some reason
        self.color_sensor_motor.position = 0
        
    #flipper functions
    def flip_cube(self):
        self.move_on_cube()
        self.move_flipper(90, 20)
        sleep(0.5)
        self.move_flipper(-90,40)
        sleep(0.2)
    def move_on_cube(self):
        if not self.on_cube:
            self.move_flipper(90, 20)
            self.on_cube = True
    def move_off_cube(self):
        if self.on_cube:
            self.move_flipper(-90, 15)
            self.on_cube = False  
    def move_flipper(self, deg, speed=20): #negative is down and positive is up #set default flipper speed here
        self.flipper_motor.on_for_degrees(speed=speed, degrees=deg)

    def normalize(self, x):
        if x<0:
            return -1
        return 1
        
    #rotator functions
    def rotate_cube(self, deg, speed=80): #positive is with the clock
        self.move_off_cube()
        self.rotate_cube_raw(deg,speed)
    def rotate_cube_raw(self, deg, speed): #positive is with the clock
        self.rotator_motor.on_for_degrees(speed=speed, degrees=deg*3)
    def rotate_bottom(self, deg, speed=80):
        self.move_on_cube()
        margin = 20*self.normalize(deg) #the extra spin to remove the wiggle room
        self.rotate_cube_raw(deg+margin,speed)
        self.rotate_cube_raw(-margin,speed)
        
        
    def do_moves(self, moves=[0]): #0: flip, 1: 90, -1: -90, 2: b 90, -2, b -90, 3: 180, 4: b 180
        for move in moves:
            print((self.rotator_motor.position/(3*90))%4)
            if move == 0:
                self.flip_cube()
            elif abs(move) == 1:
                self.rotate_cube(move*90)
            elif abs(move) == 2:
                self.rotate_bottom(45*move)
            elif move == 3:
                self.rotate_cube(180)
            elif move == 4:
                self.rotate_bottom(180)
        self.move_off_cube()
        
    def generate_moves(self, moves): #in: list of strings, standard rubiks notation, out: do_moves() moves notation
        out = []
        
        flipper_facing = 3
        front_facing = 1
        down_facing = 0 
        str_to_face = {
            "D": 0,
            "F": 1,
            "U": 5,
            "B": 4,
            "L": 3,
            "R": 2
        } #opposite face = 5-face
        
        for move_raw in moves:
                
            move = str_to_face[move_raw[0]]

            #get right face to bottom
            if move == 5-down_facing: #current U
                down_facing = 5 - down_facing
                flipper_facing = 5 - flipper_facing
                
                out.append(0)
                out.append(0)
            elif move == 5-flipper_facing: #current R
                front_facing = 5-front_facing
                temp = down_facing
                down_facing = 5-flipper_facing
                flipper_facing = 5-temp
                
                out.append(3)                
                out.append(0)
            
            elif move == flipper_facing: #current L
                temp = down_facing
                down_facing = flipper_facing
                flipper_facing = 5-temp
                
                out.append(0)
                
            elif move == front_facing: #current F
                temp = down_facing
                down_facing = front_facing
                front_facing = 5-flipper_facing
                flipper_facing = 5-temp
                
                out.append(1)
                out.append(0)
                
            elif move == 5-front_facing: #current B
                temp = down_facing
                down_facing = 5-front_facing
                front_facing = flipper_facing
                flipper_facing = 5-temp
                
                out.append(-1)
                out.append(0)
                
            #rotate cube
            #inverse since cube is seen from bottom
            if move_raw[-1] == "2":
                out.append(4)
            elif move_raw[-1] == "'":
                out.append(2)
            else:
                out.append(-2)
                
        return out

    #scanning functions
    #le stolen, but tuned myself
    def get_color(self, rgb):
        hls = rgb_to_hls(*rgb)
        
        if hls[2] > -0.4:
            return Colors.WHITE

        if hls[2] < -0.8:
            return Colors.RED if rgb[0] < 140 else Colors.ORANGE

        if hls[0] < 0.25:
            return Colors.YELLOW

        return Colors.BLUE if hls[0] > 0.4 else Colors.GREEN
    
    def move_sensor_to_angle(self, angle, speed=20):
        self.color_sensor_motor.on_for_degrees(speed, angle-self.color_sensor_motor.position)
    
    def get_sensor_rgb(self):
        return self.color_sensor.raw
    
    def scan_centre(self):
        self.move_sensor_to_angle(123)
        return self.get_color(self.get_sensor_rgb())
    
    #assumes the cube is rotated 44 clockwise from each 90 deg rotation
    def scan_edge(self):
        self.move_sensor_to_angle(113)
        return self.get_color(self.get_sensor_rgb())
    
    #assumes the cube is rotated 24.66 deg clockwise from each 90 deg rotation
    def scan_corner(self):
        self.move_sensor_to_angle(101)
        return self.get_color(self.get_sensor_rgb())
    
    def move_sensor_out_of_the_way(self):
        self.move_sensor_to_angle(10)
    
    #scans face and returns it as a 3*3 matrix
    #up on the matrix is right of (extended) color sensor 
    def scan_face(self):
        out = [
            [-1, -1, -1],
            [-1, -1, -1],
            [-1, -1, -1]
        ]
        
        loop_dictionary = {
        0: [[2, 2], [1, 2]],
        1: [[0, 2], [0, 1]],
        2: [[0, 0], [1, 0]],
        3: [[2, 0], [2, 1]]
    }
        
        out[1][1] = self.scan_centre()
        self.rotate_cube(CORNER_ROTATOR_SCAN_ANGLE)
        for i in range(4):
            current_out_index = loop_dictionary[i]
            sleep(0.2)
            out[current_out_index[0][0]][current_out_index[0][1]] = self.scan_corner()
            self.rotate_cube(EDGE_ROTATOR_SCAN_ANGLE-CORNER_ROTATOR_SCAN_ANGLE)
            sleep(0.2)
            out[current_out_index[1][0]][current_out_index[1][1]] = self.scan_edge()
            self.rotate_cube(90-EDGE_ROTATOR_SCAN_ANGLE+CORNER_ROTATOR_SCAN_ANGLE)
        
        self.rotate_cube(-CORNER_ROTATOR_SCAN_ANGLE)
        self.move_sensor_out_of_the_way()
        return out
    
    def scan_cube(self):
        self.scan_centre()
        print(self.color_sensor_motor.position)
        self.move_sensor_to_scan_edge()
        pass
        
def main():
    bot = Bot()
    bot.rotator_motor.position = 0
    print(bot.scan_face())
    #bot.rotate_cube(EDGE_ROTATOR_SCAN_ANGLE)
    #print(bot.scan_edge())
    #sleep(1)
    #bot.rotate_cube(-EDGE_ROTATOR_SCAN_ANGLE)
    while True:
        try:
            #print(rgb_to_hls(*bot.color_sensor.raw)[2])
            #print(bot.rotator_motor.position/3, bot.color_sensor_motor.position)
            #print(Colors.to_string[bot.get_color(bot.color_sensor.raw)])
            pass
        except:
            print("err")
    

if (__name__ == "__main__"):
    main()
