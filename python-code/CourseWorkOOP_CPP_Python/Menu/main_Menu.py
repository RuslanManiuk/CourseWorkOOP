from Menu.menu import Menu

class MainMenu(Menu):
    def __init__(self, screen):
        options = ["Грати", "Налаштування", "Вихід"]
        super().__init__(screen, options, "Чотири в ряд")