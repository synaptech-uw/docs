import pyautogui as move

class MoveCursor:

    def __init__(self):
        super().__init__()
        self._direction_list = ["Up", "Down", "Left", "Right"]
        self._current_dir_index = -1
        self._command = ""

    def action(self, command):
        
        self._command = command
        if self._command == "L":
            self._current_dir_index += 1
            if self._current_dir_index > 3:
                self._current_dir_index = 0
            print("Direction Set:" + self._direction_list[self._current_dir_index])
        if self._command == "R":
            curr_dir = self._direction_list[self._current_dir_index]
            print("going " + curr_dir)
            if curr_dir == "Up":
                move.moveRel(0, -25, duration = 0.25)
            elif curr_dir == "Down":
                move.moveRel(0, 25, duration = 0.25)
            elif curr_dir == "Left":
                move.moveRel(-25, 0, duration = 0.25)
            else:
                move.moveRel(25, 0, duration = 0.25)

#cursor = MoveCursor()
#cursor.action("L")
#cursor.action("L")
#cursor.action("L")
#cursor.action("L")
#cursor.action("R")
#cursor.action("R")
#cursor.action("L")
#cursor.action("R")
#cursor.action("R")
            
