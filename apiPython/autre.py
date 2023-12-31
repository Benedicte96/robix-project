from __future__ import division
from pygame.locals import *
import pygame
import sys
import os
import time

import roslibpy



client = roslibpy.Ros(host='telo-robot.local', port=9090)
client.run()

print(client.is_connected)
print(122)

talker = roslibpy.Topic(client, '/cmd_vel', 'geometry_msgs/Twist')

os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"

class joystick_handler(object):
    def _init_(self, id):
        self.id = id
        self.joy = pygame.joystick.Joystick(id)
        self.name = self.joy.get_name()
        self.joy.init()
        self.numaxes = self.joy.get_numaxes()

        self.axis = []
        for i in range(self.numaxes):
            self.axis.append(self.joy.get_axis(i))


class joystick_controller(object):
    class program:
        "Program metadata"
        name = "Remote Control Joystick"
        version = "1.0.0"
        author = "TOURE Vassindou"
        description = "Based on denilsonsa/pygame-joystick-test"
        nameversion = name + " " + version


    def init(self):
        pygame.init()
        # self.clock = pygame.time.Clock()
        self.joycount = pygame.joystick.get_count()
        if self.joycount == 0:
            print(
                "This program only works with at least one joystick plugged in. No joysticks were detected.")
            self.quit(1)
        self.joy = []
        for i in range(self.joycount):
            self.joy.append(joystick_handler(i))


    def run(self):
        speed = 0
        twist = roslibpy.Message({ 'linear':{'x':0,'y':0,'z':0}, 'angular':{'x':0,'y':0,'z':0}})
        print(self.program.nameversion)
        while True:
            for event in [pygame.event.wait(), ] + pygame.event.get():
                if event.type == QUIT:
                    self.quit()
                elif event.type == KEYDOWN and event.key in [K_ESCAPE, K_q]:
                    self.quit()
                elif event.type == JOYAXISMOTION:
                    self.joy[event.joy].axis[event.axis] = event.value
                    print(event.axis,event.value)
                    self.joy[event.joy].axis[event.axis] = event.value
                    axis = event.axis
                    value = event.value
                    if axis == 1:
                        if(abs(value) < 0.09):
                            #twist.linear.x = 0
                            twist = roslibpy.Message({ 'linear':{'x':0,'y':0,'z':0}, 'angular':{'x':0,'y':0,'z':0}})
                        else:
                            #twist.linear.x = value * speed
                            twist = roslibpy.Message({ 'linear':{'x':value * speed,'y':0,'z':0}, 'angular':{'x':0,'y':0,'z':0}})
                    elif axis == 2:
                        if(abs(value) < 0.09):
                            #twist.angular.z = 0
                            twist = roslibpy.Message({ 'linear':{'x':0,'y':0,'z':0}, 'angular':{'x':0,'y':0,'z':0}})
                        else:
                            #twist.angular.z = value * speed
                            twist = roslibpy.Message({ 'linear':{'x':0,'y':0,'z':0}, 'angular':{'x':0,'y':0,'z':value * speed}})
                    elif axis == 3:
                        speed = -1 * (1 - value)
                    #rate.sleep()
                    talker.publish(roslibpy.Message(twist))

    def quit(self, status=0):
        pygame.quit()
        sys.exit(status)


if __name__ == "_main_":
    program = joystick_controller()
    program.init()
    program.run()


#

# while client.is_connected:
#     talker.publish(roslibpy.Message({'data': 'Hello World!'}))
#     print('Sending message...')
#     time.sleep(1)

# talker.unadvertise()

# client.terminate()