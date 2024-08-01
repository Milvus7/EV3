#!/usr/bin/env python3

from time import sleep
from colorsys import rgb_to_hls

#import cube

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
    
class Bot():
    def __init__(self):
        self.on_cube = False
        
        self.color_sensor = ColorSensor(INPUT_1)
        self.flipper_motor = LargeMotor(OUTPUT_A)
        self.sensor_motor = MediumMotor(OUTPUT_B)
        self.rotator_motor = LargeMotor(OUTPUT_D)
        
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

        if hls[0] < 0.2:
            return Colors.YELLOW

        return Colors.BLUE if hls[0] > 0.4 else Colors.GREEN
    
    def scan_cube(self):
        pass
        
def main():
    bot = Bot()
    while True:
        try:
            print(bot.color_sensor.raw, Colors.to_string[bot.get_color(bot.color_sensor.raw)])
            #print(Colors.to_string[bot.get_color(bot.color_sensor.raw)])
        except:
            print("err")
    

if (__name__ == "__main__"):
    main()
