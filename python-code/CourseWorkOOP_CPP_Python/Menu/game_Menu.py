from Menu.menu import Menu

class GameMenu(Menu):
    def __init__(self, screen):
        options = ["З комп'ютером","1 на 1","Повернутися"]
        super().__init__(screen, options, "Чотири в ряд")