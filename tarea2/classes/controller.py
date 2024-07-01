#Clase de controlador Global
class Controller:
    def __init__(self):
        self.view = 0
        self.right_flipper_rotating = False
        self.left_flipper_rotating = False
        self.alpha_1 = 0 #Rotacion de flipper 1
        self.alpha_2 = 0 #Rotacion flipper 2
        self.newBall = False

    def change_view(self):
        self.view = (self.view+1)%2
    def start_right_flipper(self):
        self.right_flipper_rotating = True
    def start_left_flipper(self):
        self.left_flipper_rotating = True
    def stop_right_flipper(self):
        self.right_flipper_rotating = False
    def stop_left_flipper(self):
        self.left_flipper_rotating = False
    def generateBall(self):
        self.newBall = True
