#Clase de controlador
class Controller:
    def __init__(self):
        self.view = 0 #True para proyeccion ortografica y False para proyeccion en perspectiva
        self.x = 0
        self.z = 0
        self.y = 0

    def change_view(self):
        view_actual = self.view
        self.view = (view_actual+1)%2