import pyautogui as move
from threading import Thread
from graphics import *

WIDTH = 350
HEIGHT = 350
TRIANGLE_SIZE = 50

class MoveCursor:

    def __init__(self):
        super().__init__()
        self._direction_list = ["Up", "Down", "Left", "Right"]
        self._current_dir_index = -1
        self._command = ""
        self.threads = []
        self.win = GraphWin("Direction", WIDTH, HEIGHT)
        self.arrows = []
        self.draw(-1)

    def check_direction(self):
        for a in self.arrows:
            a.setFill('blue')
        if self._current_dir_index != -1:
            self.arrows[self._current_dir_index].setFill('yellow')

    def update_direction(self, idx):
        for a in self.arrows:
            a.setFill('blue')
        if idx != -1:
            self.arrows[idx].setFill('yellow')

    def draw(self, idx):
        up_arrow = Polygon([Point(WIDTH/2, 0), Point(WIDTH/2-TRIANGLE_SIZE, TRIANGLE_SIZE),
            Point(WIDTH/2+TRIANGLE_SIZE, TRIANGLE_SIZE)])
        down_arrow = Polygon([Point(WIDTH/2, HEIGHT), Point(WIDTH/2-TRIANGLE_SIZE, HEIGHT-TRIANGLE_SIZE),
            Point(WIDTH/2+TRIANGLE_SIZE, HEIGHT-TRIANGLE_SIZE)])
        left_arrow = Polygon([Point(0, WIDTH/2), Point(TRIANGLE_SIZE, WIDTH/2+TRIANGLE_SIZE),
            Point(TRIANGLE_SIZE, WIDTH/2-TRIANGLE_SIZE)])
        right_arrow = Polygon([Point(WIDTH, WIDTH/2), Point(WIDTH-TRIANGLE_SIZE, WIDTH/2+TRIANGLE_SIZE),
            Point(WIDTH-TRIANGLE_SIZE, WIDTH/2-TRIANGLE_SIZE)])

        self.arrows = [up_arrow, down_arrow, left_arrow, right_arrow]
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
            if curr_dir == "Up":
                move.moveRel(0, -100, duration = 0.2)
            elif curr_dir == "Down":
                move.moveRel(0, 100, duration = 0.2)
            elif curr_dir == "Left":
                move.moveRel(-100, 0, duration = 0.2)
            else:
                move.moveRel(100, 0, duration = 0.2)

    def start_action(self, command):
        thread = Thread(target = self.action, args = (command, ))
        thread.start()


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
            
