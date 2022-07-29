from signal import pause

from gpiozero import Button

from .ledmatrix import Matrix


class DirectionPad:
    def __init__(self, directions, matrix=None):
        self.matrix = matrix
        self.up = directions["up"]
        self.left = directions["left"]
        self.down = directions["down"]
        self.right = directions["right"]

        self.x = 0
        self.y = 0

        self.matrix.selectPixel(self.x, self.y)

    def move_up(self):
        if self.x > 0:
            self.x = self.x-1
            self.matrix.selectPixel(self.x, self.y)

    def move_down(self):
        if self.x < 7:
            self.x = self.x+1
            self.matrix.selectPixel(self.x, self.y)

    def move_left(self):
        if self.y > 0:
            self.y = self.y-1
            self.matrix.selectPixel(self.x, self.y)

    def move_right(self):
        if self.y < 7:
            self.y = self.y+1
            self.matrix.selectPixel(self.x, self.y)
    
    def processDPAD(self):
        self.up.when_pressed = self.move_up
        self.left.when_pressed = self.move_left
        self.down.when_pressed = self.move_down
        self.right.when_pressed = self.move_right


if __name__ == "__main__":
    mat_rows = [21, 8, 26, 12, 10, 19, 9, 6]
    mat_cols = [7, 11, 5, 20, 13, 16, 25, 24]

    mat8x8 = Matrix(mat_rows, mat_cols)

    directions = {
        'up': Button(4),
        'left': Button(2),
        'down': Button(3),
        'right': Button(17),
    }

    dpad = DirectionPad(directions, mat8x8)

    dpad.processDPAD()

    pause()
