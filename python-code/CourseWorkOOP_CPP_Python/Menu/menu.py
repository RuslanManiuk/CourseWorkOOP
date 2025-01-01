import pygame
import sys

class Menu:
    def __init__(self, screen, options, title):
        """
        Ініціалізація меню.

        :param screen: Екран для відображення меню.
        :param options: Список опцій меню.
        :param title: Заголовок меню.
        """
        self.screen = screen
        self.options = options
        self.title = title
        self.selected_option = 0
        self.button_scales = [1.0] * len(options)  # Масштаби кнопок для кожної опції

        # Кольори для градієнтного фону
        self.bg_top_color = (0, 0, 50)
        self.bg_bottom_color = (0, 0, 150)

        self.set_colors()
        self.load_fonts()

    def set_colors(self):
        """
        Встановлює кольори для різних елементів меню.
        """
        self.BUTTON_COLOR = (50, 100, 200)
        self.BUTTON_SHADOW = (30, 30, 60)
        self.BUTTON_HOVER = (100, 150, 250)
        self.BUTTON_PRESSED = (80, 130, 220)
        self.TEXT_COLOR = (255, 255, 255)
        self.TITLE_COLOR = (255, 255, 255)
        self.TITLE_SHADOW = (30, 30, 60)
        self.BORDER_WIDTH = 10
        self.BUTTON_BORDER_COLOR = (200, 200, 255)

    def load_fonts(self):
        """
        Завантажує шрифти для тексту та заголовків.
        """
        self.title_font = pygame.font.SysFont("arial", 60, bold=True)
        self.button_font = pygame.font.SysFont("arial", 40)

    def draw_gradient(self):
        """
        Малює градієнтний фон.
        """
        for y in range(self.screen.get_height()):
            ratio = y / self.screen.get_height()
            r = int(self.bg_top_color[0] * (1 - ratio) + self.bg_bottom_color[0] * ratio)
            g = int(self.bg_top_color[1] * (1 - ratio) + self.bg_bottom_color[1] * ratio)
            b = int(self.bg_top_color[2] * (1 - ratio) + self.bg_bottom_color[2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.screen.get_width(), y))

    def draw_3d_title(self, text, font, base_color, shadow_color, shadow_offset=5):
        """
        Малює 3D-заголовок із текстом та тінню.

        :param text: Текст заголовку
        :param font: Шрифт Pygame
        :param base_color: Колір основного тексту
        :param shadow_color: Колір тіні
        :param shadow_offset: Зміщення тіні
        """
        # Рендеринг тіні
        shadow_surface = font.render(text, True, shadow_color)
        shadow_pos = (
            self.screen.get_width() // 2 - shadow_surface.get_width() // 2 + shadow_offset,
            50 + shadow_offset
        )
        self.screen.blit(shadow_surface, shadow_pos)

        # Рендеринг основного тексту
        text_surface = font.render(text, True, base_color)
        text_pos = (
            self.screen.get_width() // 2 - text_surface.get_width() // 2,
            50
        )
        self.screen.blit(text_surface, text_pos)

    def fit_text_to_button(self, text, button_width):
        """
        Зменшує розмір шрифту, якщо текст не вміщується у кнопку.

        :param text: Текст для перевірки.
        :param button_width: Ширина кнопки.
        :return: Відрендерений текст поверхня з відповідним розміром шрифту.
        """
        font_size = 40
        while font_size > 10:
            font = pygame.font.SysFont("arial", font_size)
            text_surface = font.render(text, True, self.TEXT_COLOR)
            if text_surface.get_width() <= button_width - 20:  # Відступи від країв
                return text_surface, font
            font_size -= 2
        font = pygame.font.SysFont("arial", 10)
        return font.render(text, True, self.TEXT_COLOR), font

    def draw_button_with_effects(self, text, rect, state="normal", index=0):
        """
        Малює кнопку з ефектами в синьо-чорній гамі.

        :param text: Текст кнопки.
        :param rect: Прямокутник кнопки.
        :param state: Стан кнопки (normal, hover, pressed).
        :param index: Індекс кнопки.
        """
        scale = self.button_scales[index]
        if state == "hover":
            self.button_scales[index] = min(1.1, scale + 0.01)
        else:
            self.button_scales[index] = max(1.0, scale - 0.01)

        button_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

        # Тінь кнопки
        shadow_rect = pygame.Rect(5, 5, rect.width, rect.height)
        pygame.draw.rect(button_surf, self.BUTTON_SHADOW, shadow_rect, border_radius=self.BORDER_WIDTH)

        # Основна кнопка
        button_rect = pygame.Rect(0, 0, rect.width, rect.height)
        color = {
            "normal": self.BUTTON_COLOR,
            "hover": self.BUTTON_HOVER,
            "pressed": self.BUTTON_PRESSED
        }[state]
        pygame.draw.rect(button_surf, color, button_rect, border_radius=self.BORDER_WIDTH)

        # Відображення тексту
        text_surface, font = self.fit_text_to_button(text, rect.width)
        text_rect = text_surface.get_rect(center=(rect.width // 2, rect.height // 2))
        button_surf.blit(text_surface, text_rect)

        # Масштабування кнопки
        scaled_surf = pygame.transform.scale(button_surf, (
            int(button_surf.get_width() * scale),
            int(button_surf.get_height() * scale)
        ))
        scaled_rect = scaled_surf.get_rect(center=rect.center)

        self.screen.blit(scaled_surf, scaled_rect)

    def display(self):
        """
        Відображає меню та обробляє події.
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
                button_text = option

                button_rect = pygame.Rect(
                    button_x, button_y + i * (button_height + button_spacing), button_width, button_height
                )
                state = "hover" if button_rect.collidepoint(pygame.mouse.get_pos()) else "normal"

                self.draw_button_with_effects(button_text, button_rect, state, i)

            # Обробка подій
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
                        option = self.options[self.selected_option]
                        return option
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, option in enumerate(self.options):
                        button_rect = pygame.Rect(
                            button_x, button_y + i * (button_height + button_spacing), button_width, button_height
                        )
                        if button_rect.collidepoint(event.pos):
                           return option

            pygame.display.flip()
            clock.tick(30)
