import pygame
import sys

from Menu.menu import Menu
from Game.with_bot_Game import GameWithAI

class BotGameMenu(Menu):
    def __init__(self, screen):
        self.field_sizes = ["4x4", "4x5", "5x6", "6x7", "7x8", "8x9", "9x10"]
        self.current_size_index = 0
        options = ["Легкий", "Середній", "Важкий", "Розмір поля", "Повернутися"]
        self.difficulty_map = {
            "Легкий": "easy",
            "Середній": "medium",
            "Важкий": "hard",
        }
        super().__init__(screen, options, "Гра з комп'ютером")

    def get_field_size(self):
        """
        Повертає поточний вибраний розмір поля у вигляді (rows, cols).
        """
        return tuple(map(int, self.field_sizes[self.current_size_index].split('x')))

    def run(self):
        """
        Розширює метод display для додавання логіки роботи меню.
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

            # Визначення розмірів кнопок
            screen_height = self.screen.get_height()
            screen_width = self.screen.get_width()

            max_button_height = 70
            top_spacing = 200  # Простір для заголовка
            bottom_spacing = 50  # Простір знизу

            # Максимальна доступна висота для кнопок і відступів
            available_height = screen_height - top_spacing - bottom_spacing

            # Визначення висоти кнопок та міжкнопкового відступу
            button_height = min(max_button_height, available_height // len(self.options))
            button_spacing = max(10, (available_height - button_height * len(self.options)) // (len(self.options) - 1))

            # Визначення ширини кнопок
            button_width = screen_width // 3
            button_x = screen_width // 2 - button_width // 2

            # Визначення верхнього відступу для вирівнювання кнопок по центру
            button_y = top_spacing

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
                        if result == "back":
                            return "back"
                        elif result:
                            return result
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, option in enumerate(self.options):
                        button_rect = pygame.Rect(
                            button_x, button_y + i * (button_height + button_spacing), button_width, button_height
                        )
                        if button_rect.collidepoint(event.pos):
                            result = self.handle_option_selection(option)
                            if result == "back":
                                return "back"
                            elif result:
                                return result

            pygame.display.flip()
            clock.tick(30)

    def handle_option_selection(self, option):
        """
        Обробляє вибір опції.

        Параметри:
            option (str): Вибрана опція меню

        Повертає:
            tuple: (складність, рядки, стовпці) або "back" для повернення
        """
        if option == "Розмір поля":
            self.current_size_index = (self.current_size_index + 1) % len(self.field_sizes)
            return None  # Повертаємося до меню
        elif option in ["Легкий", "Середній", "Важкий"]:
            rows, cols = self.get_field_size()
            difficulty = self.difficulty_map[option]
            return difficulty, rows, cols
        elif option == "Повернутися":
            return "back"
