import pygame
import sys

from Menu.menu import Menu
from Game.One_on_One_Game import OneOnOneGame

class OneOnOneMenu(Menu):
    def __init__(self, screen):
        self.field_sizes = ["4x4", "4x5", "5x6", "6x7", "7x8", "8x9", "9x10"]
        self.current_size_index = 0  # Індекс поточного розміру
        options = ["Почати гру", "Розмір поля", "Повернутися"]
        super().__init__(screen, options, "1 на 1")

    def get_field_size(self):
        """
        Повертає поточний вибраний розмір поля у вигляді (rows, cols).
        """
        return tuple(map(int, self.field_sizes[self.current_size_index].split('x')))

    def run(self):
        """
        Відображає меню і обробляє вибір користувача.
        """
        clock = pygame.time.Clock()

        while True:
            self.draw_gradient()
            self.draw_3d_title(
                self.title,
                self.title_font,
                self.TITLE_COLOR,
                (50, 50, 50),
                5
            )

            button_width = self.screen.get_width() // 3
            button_height = 70
            button_spacing = 20
            button_x = self.screen.get_width() // 2 - button_width // 2
            button_y = 200

            for i, option in enumerate(self.options):
                display_text = option
                if option == "Розмір поля":
                    display_text = f"{option} ({self.field_sizes[self.current_size_index]})"

                button_rect = pygame.Rect(
                    button_x, button_y + i * (button_height + button_spacing), button_width, button_height
                )
                state = "hover" if button_rect.collidepoint(pygame.mouse.get_pos()) else "normal"

                self.draw_button_with_effects(display_text, button_rect, state, i)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        result = self.handle_option_selection(self.options[self.selected_option])
                        if result:
                            return result
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, option in enumerate(self.options):
                        button_rect = pygame.Rect(
                            button_x, button_y + i * (button_height + button_spacing), button_width, button_height
                        )
                        if button_rect.collidepoint(event.pos):
                            result = self.handle_option_selection(option)
                            if result:
                                return result

            pygame.display.flip()
            clock.tick(30)

    def handle_option_selection(self, option):
        """
        Обробляє вибір опції, включаючи зміну розміру поля.
        """
        if option == "Розмір поля":
            # Циклічне перемикання розмірів поля
            self.current_size_index = (self.current_size_index + 1) % len(self.field_sizes)
        elif option == "Почати гру":
            # Повертає команду для запуску гри
            rows, cols = self.get_field_size()
            return "start_game", rows, cols
        elif option == "Повернутися":
            # Повертає команду для повернення
            return "back"

