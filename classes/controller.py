#Clase de controlador Global
class Controller:
    def __init__(self):
        self.view = 0

    def change_view(self):
        self.view = (self.view+1)%2
