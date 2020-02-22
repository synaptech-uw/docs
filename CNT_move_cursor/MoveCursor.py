import pyautogui as move

class MoveCursor:

    direction_list = ["Up", "Down", "Left", "Right"]
    curr_dir_index = -1
    movement = 0
    
    def __init__(self, command):
        super().__init__()
        self._command = command
        if self._command == "L":
            current_dir_index += 1
            if current_dir_index > 3:
                current_dir_index = 0
        if self._command == "R":
            curr_dir = direction_list[current_dir_index]
            if curr_dir == "Up":
                move.moveRel(0, 10, duration = 1)
            elif curr_dir == "Down":
                move.moveRel(0, -10, duration = 1)
            elif curr_dir == "Left":
                move.moveRel(-10, 0, duration = 1)
            else:
                move.moveRel(10, 0, duration = 1)

            
