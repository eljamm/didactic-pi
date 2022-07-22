import RPi.GPIO as GPIO
from time import sleep


class Matrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)

        for row in self.rows:
            GPIO.setup(row, GPIO.OUT, initial=GPIO.LOW)
        for col in self.cols:
            GPIO.setup(col, GPIO.OUT, initial=GPIO.HIGH)

    def selectRow(self, x):
        for row in self.rows:
            if row == self.rows[x]:
                GPIO.output(row, 1)
            else:
                GPIO.output(row, 0)

    def selectColumn(self, y):
        for col in self.cols:
            if col == self.cols[y]:
                GPIO.output(col, 0)
            else:
                GPIO.output(col, 1)

    def scan(self):
        for i in range(8):
            self.selectRow(i)
            for j in range(8):
                self.selectColumn(j)
                sleep(0.1)

    def setLED(self, y, state):
        for col in self.cols:
            if col == self.cols[y]:
                GPIO.output(col, state)
                break

    def clearMatrix(self):
        for i in range(8):
            self.selectRow(i)
            for j in range(8):
                self.setLED(j, 1)
        GPIO.cleanup()

    def drawShape(self, shape):
        for i in range(8):
            self.selectRow(i)
            for j in range(8):
                self.setLED(j, shape[i][j])

            sleep(0.002)

    def processMatrix(self, message):
        if isinstance(message, list):
            rows, cols = (8, 8)
            shape = [[1]*cols]*rows

            shape = []
            for i in range(8):
                shape_tmp = []
                for j in range(8):
                    shape_tmp.append(message[j][i])
                shape.append(shape_tmp)

            self.drawShape(shape)


if __name__ == "__main__":
    rows = [7, 18, 9, 24, 2, 10, 3, 27]
    cols = [23, 4, 17, 8, 22, 25, 15, 14]

    shape = [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 1, 1, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 0, 0, 0, 1, 1],
        [1, 1, 1, 0, 0, 1, 1, 1],
    ]

    mat8x8 = Matrix(rows, cols)

    while True:
        try:
            mat8x8.drawShape(shape)

        except KeyboardInterrupt:
            print("\nExiting Program")
            mat8x8.clearMatrix()
            break
