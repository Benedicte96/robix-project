from __future__ import division
from pygame.locals import *
import pygame
import sys
import os
import time
import requests
import roslibpy

# Initialisation de la variable running
running = True


# Initialisation de la connexion ROS

response = requests.get('http://127.0.0.1:5000/api/robot-host')
if response.status_code == 200:
    data = response.json()
    print(data['robotHost'])
    print(data['param'])
else:
    print("La requête n'a pas abouti avec le code de statut :", response.status_code)
    print("Contenu de la réponse :", response.text)


#client = roslibpy.Ros(host='telo-robot.local', port=9090)
client = roslibpy.Ros(host=data['robotHost'], port=9090)

client.run()
print(client.is_connected)

# Initialisation du topic ROS pour envoyer des commandes de mouvement
talker = roslibpy.Topic(client, data['param'], 'geometry_msgs/Twist')

# Autoriser les événements de joystick en arrière-plan
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"

class JoystickHandler:
    def __init__(self, id):
        self.id = id
        self.joy = pygame.joystick.Joystick(id)
        self.name = self.joy.get_name()
        self.joy.init()
        self.numaxes = self.joy.get_numaxes()
        self.axis = []
        for i in range(self.numaxes):
            self.axis.append(self.joy.get_axis(i))

class JoystickController:
    def __init__(self):
        self.program = {
            "name": "Remote Control Joystick",
            "version": "1.0.0",
            "author": "TOURE Vassindou",
            "description": "Based on denilsonsa/pygame-joystick-test"
        }

    def init(self):
        pygame.init()
        self.joycount = pygame.joystick.get_count()
        if self.joycount == 0:
            print("Ce programme ne fonctionne qu'avec au moins un joystick connecté. Aucun joystick n'a été détecté.")
            self.quit(1)
        self.joy = []
        for i in range(self.joycount):
            self.joy.append(JoystickHandler(i))

    def run(self):
        speed = 0
        twist = roslibpy.Message({'linear': {'x': 0, 'y': 0, 'z': 0}, 'angular': {'x': 0, 'y': 0, 'z': 0}})
        print(self.program['name'] + " " + self.program['version'])
        while True:
            for event in [pygame.event.wait(), ] + pygame.event.get():
                if event.type == QUIT:
                    self.quit()
                elif event.type == KEYDOWN and event.key in [K_ESCAPE, K_q]:
                    self.quit()
                elif event.type == JOYAXISMOTION:
                    self.joy[event.joy].axis[event.axis] = event.value
                    print(event.axis, event.value)
                    axis = event.axis
                    value = event.value
                    if axis == 1:
                        if abs(value) < 0.09:
                            twist = roslibpy.Message({'linear': {'x': 0, 'y': 0, 'z': 0}, 'angular': {'x': 0, 'y': 0, 'z': 0}})
                        else:
                            twist = roslibpy.Message({'linear': {'x': value * speed, 'y': 0, 'z': 0}, 'angular': {'x': 0, 'y': 0, 'z': 0}})
                    elif axis == 2:
                        if abs(value) < 0.09:
                            twist = roslibpy.Message({'linear': {'x': 0, 'y': 0, 'z': 0}, 'angular': {'x': 0, 'y': 0, 'z': 0}})
                        else:
                            twist = roslibpy.Message({'linear': {'x': 0, 'y': 0, 'z': 0}, 'angular': {'x': 0, 'y': 0, 'z': value * speed}})
                    elif axis == 3:
                        speed = -1 * (1 - value)

                    talker.publish(roslibpy.Message(twist))

    def quit(self, status=0):
        pygame.quit()
        sys.exit(status)


# class JoystickController:
#     # ...
#     def run(self):
#         global running
#         # ...
#         while running:
#             for event in [pygame.event.wait(), ] + pygame.event.get():
#                 if event.type == QUIT:
#                     self.quit()
#                 elif event.type == KEYDOWN and event.key in [K_ESCAPE, K_q]:
#                     self.quit()
#                 elif event.type == JOYAXISMOTION:
#                     # ...
#                     talker.publish(roslibpy.Message(twist))

    def quit(self, status=0):
        global running
        running = False
        pygame.quit()
        sys.exit(status)


if __name__ == "__main__":
    program = JoystickController()
    program.init()
    program.run()


# from __future__ import division
# from msilib.schema import SelfReg
# from typing import Self
# from pygame.locals import *
# import pygame
# import sys
# import os
# import time
# import requests
# import roslibpy

# # Initialisation de la variable running
# running = True

# # Initialisation de la connexion ROS
# response = requests.get('http://127.0.0.1:5000/api/robot-host')
# if response.status_code == 200:
#     data = response.json()
#     print(data['robotHost'])
#     print(data['param'])
# else:
#     print("La requête n'a pas abouti avec le code de statut :", response.status_code)
#     print("Contenu de la réponse :", response.text)

# #client = roslibpy.Ros(host='telo-robot.local', port=9090)
# client = roslibpy.Ros(host=data['robotHost'], port=9090)

# client.run()
# print(client.is_connected)

# # Initialisation du topic ROS pour envoyer des commandes de mouvement
# talker = roslibpy.Topic(client, data['param'], 'geometry_msgs/Twist')

# # Autoriser les événements de joystick en arrière-plan
# os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"


# class JoystickHandler:
#   #

# class JoystickController:
#     def __init__(self):
#         self.program = {
#             "name": "Remote Control Joystick",
#             "version": "1.0.0",
#             "author": "TOURE Vassindou",
#             "description": "Based on denilsonsa/pygame-joystick-test"
#         }
#         self.joy = []
#         self.joycount = 0

#     def init(self):
#         pygame.init()
#         self.joycount = pygame.joystick.get_count()
#         if self.joycount == 0:
#             print("Ce programme ne fonctionne qu'avec au moins un joystick connecté. Aucun joystick n'a été détecté.")
#             self.quit(1)
#         for i in range(self.joycount):
#             self.joy.append(JoystickHandler(i))

#     def run(self):
#         global running
#         speed = 0
#         twist = roslibpy.Message({'linear': {'x': 0, 'y': 0, 'z': 0}, 'angular': {'x': 0, 'y': 0, 'z': 0}})
#         print(self.program['name'] + " " + self.program['version'])
#         while running:
#             for event in [pygame.event.wait(), ] + pygame.event.get():
#                 if event.type == QUIT:
#                     self.quit()
#                 elif event.type == KEYDOWN and event.key in [K_ESCAPE, K_q]:
#                     self.quit()
#                 elif event.type == JOYAXISMOTION:
#                     self.joy[event.joy].axis[event.axis] = event.value
#                     print(event.axis, event.value)
#                     axis = event.axis
#                     value = event.value
#                     if axis == 1:
#                         if abs(value) < 0.09:
#                             twist = roslibpy.Message({'linear': {'x': 0, 'y': 0, 'z': 0}, 'angular': {'x': 0, 'y': 0, 'z': 0}})
#                         else:
#                             twist = roslibpy.Message({'linear': {'x': value * speed, 'y': 0, 'z': 0}, 'angular': {'x': 0, 'y': 0, 'z': 0}})
#                     elif axis == 2:
#                         if abs(value) < 0.09:
#                             twist = roslibpy.Message({'linear': {'x': 0, 'y': 0, 'z': 0}, 'angular': {'x': 0, 'y': 0, 'z': 0}})
#                         else:
#                             twist = roslibpy.Message({'linear': {'x': 0, 'y': 0, 'z': 0}, 'angular': {'x': 0, 'y': 0, 'z': value * speed}})
#                     elif axis == 3:
#                         speed = -1 * (1 - value)

#                     talker.publish(roslibpy.Message(twist))

#     def quit(self, status=0):
#         global running
#         running = False
#         pygame.quit()
#         sys.exit(status)


# if __name__ == "__main__":
#     program = JoystickController()
#     program.init()
#     program.run()
