class Drive:
    def __init__(self, rightWheel, leftWheel):
        self.rightWheel = rightWheel
        self.leftWheel = leftWheel

    def forward(self, speed):
        self.rightWheel.forward(speed)
        self.leftWheel.forward(speed)

    def reverse(self, speed):
        self.rightWheel.backwards(speed)
        self.leftWheel.backwards(speed)

    def stop(self):
        self.rightWheel.stop()
        self.leftWheel.stop()

    def right(self, speed):
        self.rightWheel.forward(speed)
        self.leftWheel.backwards(speed)

    def left(self, speed):
        self.rightWheel.backwards(speed)
        self.leftWheel.forward(speed)