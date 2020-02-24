import pyautogui as move
from threading import Thread
from graphics import *

WIDTH = 350
HEIGHT = 350
TRIANGLE_SIZE = 50

class MoveCursor:

    def __init__(self):
        super().__init__()
        self._direction_list = ["Up", "Right", "Down", "Left"]
        self._current_dir_index = 3
        self._command = ""
        self.threads = []
        self.win = GraphWin("Direction", WIDTH, HEIGHT)
        self.arrows = []
        self.movement = False
        self.draw(3)

    def check_direction(self):
        for i in range(len(self.arrows)):
            if i == self._current_dir_index:
                self.arrows[i].setFill('yellow')
            else:
                self.arrows[i].setFill('blue')

    def update_direction(self, idx):
        for i in range(len(self.arrows)):
            if i == idx:
                self.arrows[i].setFill('yellow')
            else:
                self.arrows[i].setFill('blue')

    def draw(self, idx):
        up_arrow = Polygon([Point(WIDTH/2, 0), Point(WIDTH/2-TRIANGLE_SIZE, TRIANGLE_SIZE),
            Point(WIDTH/2+TRIANGLE_SIZE, TRIANGLE_SIZE)])
        down_arrow = Polygon([Point(WIDTH/2, HEIGHT), Point(WIDTH/2-TRIANGLE_SIZE, HEIGHT-TRIANGLE_SIZE),
            Point(WIDTH/2+TRIANGLE_SIZE, HEIGHT-TRIANGLE_SIZE)])
        left_arrow = Polygon([Point(0, WIDTH/2), Point(TRIANGLE_SIZE, WIDTH/2+TRIANGLE_SIZE),
            Point(TRIANGLE_SIZE, WIDTH/2-TRIANGLE_SIZE)])
        right_arrow = Polygon([Point(WIDTH, WIDTH/2), Point(WIDTH-TRIANGLE_SIZE, WIDTH/2+TRIANGLE_SIZE),
            Point(WIDTH-TRIANGLE_SIZE, WIDTH/2-TRIANGLE_SIZE)])

        self.arrows = [up_arrow, right_arrow, down_arrow, left_arrow]
        for a in self.arrows:
            a.setFill('blue')
            a.draw(self.win)
        if idx != -1:
            self.arrows[idx].setFill('yellow')

    def action(self, command):

        self._command = command
        if self._command == "L":
            self._current_dir_index += 1
            if self._current_dir_index > 3:
                self._current_dir_index = 0
            self.update_direction(self._current_dir_index)
            print("Direction Set:" + self._direction_list[self._current_dir_index])
        if self._command == "R":
            curr_dir = self._direction_list[self._current_dir_index]
            print("going " + curr_dir)
            print(str(self.movement))
            while(self.movement): #Now start moving the cursor from pause
                if curr_dir == "Up":
                    move.moveRel(0, -30, duration = 0.005)
                elif curr_dir == "Down":
                    move.moveRel(0, 30, duration = 0.005)
                elif curr_dir == "Left":
                    move.moveRel(-30, 0, duration = 0.005)
                else:
                    move.moveRel(30, 0, duration = 0.005)

    def start_action(self, command):
        thread = Thread(target = self.action, args = (command, ))
        thread.start()

    def move(self, command):
        if self.movement:
            print("Setting to false in move")
            self.movement = False
        else:
            self.movement = True
            start_action(command)




#cursor = MoveCursor()
#cursor.draw(1)
#cursor.action("L")
#cursor.action("L")
#cursor.action("L")
#cursor.action("L")
#cursor.start_action("R")
#cursor.action("R")
#cursor.action("L")
#cursor.action("R")
#cursor.action("R")
            
