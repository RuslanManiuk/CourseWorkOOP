import pygame
import sys
from Menu.menu import Menu
from Music_Manager.music_Manager import MusicManager
from Configuration.class_Config import Config


class SettingsMenu(Menu):
    def __init__(self, screen, music_manager):
        options = ["Музика", "Гучність", "Розширення", "Повноекранний режим", "Повернутися"]
        super().__init__(screen, options, "Налаштування")
        self.music_manager = music_manager  # Зберігаємо переданий екземпляр

    def toggle_music(self):
        """Перемикає стан музики"""
        Config.MUSIC_ENABLED = not Config.MUSIC_ENABLED
        if Config.MUSIC_ENABLED:
            self.music_manager.unpause_music()
        else:
            self.music_manager.pause_music()
        Config.save_to_file()

    def change_volume(self):
        """Змінює рівень гучності"""
        Config.VOLUME = round((Config.VOLUME * 5 + 1) % 6) / 5

        self.music_manager.set_volume(Config.VOLUME)
        Config.save_to_file()

    def get_option_status(self, option):
        """Повертає поточний стан налаштування для відображення"""
        if option == "Музика":
            return f"[{'Грає' if Config.MUSIC_ENABLED else 'Пауза'}]"
        elif option == "Гучність":
            return f"[{int(Config.VOLUME * 100)}%]"
        elif option == "Розширення":
            return f"[{Config.RESOLUTION[0]}x{Config.RESOLUTION[1]}]"
        elif option == "Повноекранний режим":
            return f"[{'Увімк.' if Config.FULLSCREEN else 'Вимк.'}]"
        return ""

    def toggle_fullscreen(self):
        """Перемикає повноекранний режим"""
        Config.FULLSCREEN = not Config.FULLSCREEN
        if Config.FULLSCREEN:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(Config.RESOLUTION)
        Config.save_to_file()

    def change_resolution(self):
        """Змінює роздільну здатність"""
        resolutions = [(800, 600), (1280, 720), (1920, 1080)]
        try:
            current_index = resolutions.index(Config.RESOLUTION)
        except ValueError:
            current_index = 0

        Config.RESOLUTION = resolutions[(current_index + 1) % len(resolutions)]
        if not Config.FULLSCREEN:
            self.screen = pygame.display.set_mode(Config.RESOLUTION)
        Config.save_to_file()

    def display(self):
        """
        Відображає меню та обробляє події для налаштувань.
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

            # Відображення кнопок
            screen_height = self.screen.get_height()
            screen_width = self.screen.get_width()

            max_button_height = 70
            top_spacing = 200
            bottom_spacing = 50

            available_height = screen_height - top_spacing - bottom_spacing
            button_height = min(max_button_height, available_height // len(self.options))
            button_spacing = max(10, (available_height - button_height * len(self.options)) // (len(self.options) - 1))

            button_width = screen_width // 2
            button_x = screen_width // 2 - button_width // 2
            button_y = top_spacing

            for i, option in enumerate(self.options):
                display_text = option + self.get_option_status(option)
                button_rect = pygame.Rect(
                    button_x, button_y + i * (button_height + button_spacing), button_width, button_height
                )
                state = "hover" if button_rect.collidepoint(pygame.mouse.get_pos()) else "normal"
                self.draw_button_with_effects(display_text, button_rect, state, i)

            # Обробка подій
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, option in enumerate(self.options):
                        button_rect = pygame.Rect(
                            button_x, button_y + i * (button_height + button_spacing), button_width, button_height
                        )
                        if button_rect.collidepoint(event.pos):
                            if option == "Музика":
                                self.toggle_music()
                            elif option == "Гучність":
                                self.change_volume()
                            elif option == "Розширення":
                                self.change_resolution()
                            elif option == "Повноекранний режим":
                                self.toggle_fullscreen()
                            elif option == "Повернутися":
                                return "Повернутися"

            pygame.display.flip()
            clock.tick(30)