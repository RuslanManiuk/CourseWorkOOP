import pygame
import sys
import math

class ConnectFourGame:
    def __init__(self, screen, rows, cols):
        self.screen = screen
        self.rows = rows
        self.cols = cols
        self.recalculate_dimensions()

        self.board = [[0 for _ in range(cols)] for _ in range(self.rows)]
        self.current_player = 1

        # Кольори
        self.blue = (20, 9, 91)
        self.black = (0, 0, 0)
        self.dark_blue = (0, 0, 100)
        self.red = (255, 0, 0)
        self.yellow = (255, 255, 0)

        # Неонові кольори
        self.neon_blue = (0, 255, 255)  # Початковий синій колір
        self.neon_red = (255, 50, 50)
        self.neon_yellow = (255, 255, 50)

        # Поточний колір неонової рамки
        self.current_neon_color = self.neon_blue

        # Параметри неонового ефекту
        self.neon_width = 4
        self.glow_intensity = 3

        # Параметри пульсації неону
        self.pulse_speed = 0.05
        self.pulse_time = 0
        self.pulse_min = 0.7
        self.pulse_max = 1.0

        # Параметри анімації
        self.animation_speed = 15
        self.is_animating = False
        self.animation_piece = None
        self.animation_y = 0
        self.target_y = 0
        self.target_row = 0
        self.target_col = 0

        # Параметри анімації кольору
        self.color_transition_progress = 0
        self.start_color = self.neon_blue
        self.target_color = self.neon_blue

        self.hover_col = None

    def interpolate_color(self, color1, color2, progress):
        """Інтерполює між двома кольорами."""
        return tuple(int(c1 + (c2 - c1) * progress) for c1, c2 in zip(color1, color2))

    def get_current_neon_color(self):
        """Повертає поточний колір неонової рамки з ефектом пульсації."""

        # Оновлення часу пульсації
        self.pulse_time += self.pulse_speed

        # Розрахунок коефіцієнту пульсації
        pulse_factor = self.pulse_min + (math.sin(self.pulse_time) + 1) * (self.pulse_max - self.pulse_min) / 2

        if self.is_animating:
            # Розрахунок прогресу на основі позиції фішки
            progress = (self.animation_y - (self.offset_y + self.square_size // 2)) / (
                        self.target_y - (self.offset_y + self.square_size // 2))
            progress = max(0, min(1, progress))  # Обмеження значення від 0 до 1

            # Інтерполяція між початковим і цільовим кольором
            current_color = self.interpolate_color(self.start_color, self.target_color, progress)
        else:
            current_color = self.current_neon_color

        # Застосування пульсації до кольору
        return tuple(int(c * pulse_factor) for c in current_color)

    def draw_neon_line(self, start_pos, end_pos):
        """Малює неонову лінію з ефектом світіння."""
        neon_color = self.get_current_neon_color()

        for i in range(self.glow_intensity, 0, -1):
            width = self.neon_width * i
            alpha = 255 // (i * 2)
            line_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            pygame.draw.line(line_surface, (*neon_color, alpha), start_pos, end_pos, width)
            self.screen.blit(line_surface, (0, 0))

    def draw_neon_border(self):
        """Малює неонову рамку навколо дошки."""
        padding = 10
        left = self.offset_x - padding
        top = self.offset_y - padding
        right = self.offset_x + self.board_width + padding
        bottom = self.offset_y + self.board_height + padding

        self.draw_neon_line((left, top), (right, top))
        self.draw_neon_line((right, top), (right, bottom))
        self.draw_neon_line((right, bottom), (left, bottom))
        self.draw_neon_line((left, bottom), (left, top))

    def start_animation(self, col):
        """Запускає анімацію падіння фішки."""
        row = None
        for r in reversed(range(self.rows)):
            if self.board[r][col] == 0:
                row = r
                break

        if row is not None:
            self.is_animating = True
            self.animation_piece = self.current_player
            self.animation_y = self.offset_y + self.square_size // 2
            self.target_row = row
            self.target_col = col
            self.target_y = self.offset_y + (row + 1) * self.square_size + self.square_size // 2

            # Встановлення початкового і цільового кольору для анімації
            self.start_color = self.neon_blue
            self.target_color = self.neon_red if self.current_player == 1 else self.neon_yellow
            return True
        return False

    def update_animation(self):
        """Оновлює стан анімації."""
        if self.is_animating:
            self.animation_y += self.animation_speed

            if self.animation_y >= self.target_y:
                self.animation_y = self.target_y
                self.board[self.target_row][self.target_col] = self.animation_piece
                self.is_animating = False

                # Встановлення кінцевого кольору рамки
                self.current_neon_color = self.target_color
                return True

        return False

    def switch_player(self):
        """Змінює поточного гравця."""
        self.current_player = 3 - self.current_player

        # Повернення до синього кольору при зміні гравця
        self.current_neon_color = self.neon_blue

    def draw_board(self):
        """Малює ігрову дошку."""

        self.draw_gradient_background()
        self.draw_neon_border()

        # Малювання дошки
        for row in range(self.rows):
            for col in range(self.cols):
                pygame.draw.rect(
                    self.screen,
                    self.blue,
                    (self.offset_x + col * self.square_size,
                     self.offset_y + (row + 1) * self.square_size,
                     self.square_size,
                     self.square_size)
                )
                pygame.draw.circle(
                    self.screen,
                    self.black,
                    (self.offset_x + col * self.square_size + self.square_size // 2,
                     self.offset_y + (row + 1) * self.square_size + self.square_size // 2),
                    self.radius
                )

        # Малювання фішок на дошці
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != 0:
                    color = self.red if self.board[row][col] == 1 else self.yellow
                    pygame.draw.circle(
                        self.screen,
                        color,
                        (self.offset_x + col * self.square_size + self.square_size // 2,
                         self.offset_y + (row + 1) * self.square_size + self.square_size // 2),
                        self.radius
                    )

        # Малювання фішки, що зависає
        self.draw_hover_piece()

        # Малювання анімованої фішки
        if self.is_animating:
            color = self.red if self.animation_piece == 1 else self.yellow
            pygame.draw.circle(
                self.screen,
                color,
                (self.offset_x + self.target_col * self.square_size + self.square_size // 2,
                 self.animation_y),
                self.radius
            )

        pygame.display.update()

    def drop_piece(self, col):
        """Додає фішку у вказану колонку з анімацією."""
        if col is None or col < 0 or col >= self.cols:
            return False

        if self.is_animating:  # Якщо анімація вже йде, ігноруємо нові ходи
            return False

        return self.start_animation(col)

    def draw_gradient_background(self):
        """Малює градієнтний фон від чорного до темно-синього."""
        height = self.screen_height
        for i in range(height):
            # Розрахунок кольору для поточного рядка
            factor = i / height
            color = (
                int(self.dark_blue[0] * factor),
                int(self.dark_blue[1] * factor),
                int(self.dark_blue[2] * factor)
            )
            pygame.draw.line(self.screen, color, (0, i), (self.screen_width, i))

    def recalculate_dimensions(self):
        """Перераховує розміри дошки відповідно до розміру екрану."""
        self.screen_width, self.screen_height = self.screen.get_size()

        # Розрахунок максимально можливого розміру клітинки
        max_square_width = self.screen_width // self.cols
        max_square_height = self.screen_height // (self.rows + 1)  # +1 для верхнього ряду

        # Вибираємо менший розмір для збереження квадратної форми
        self.square_size = min(max_square_width, max_square_height)

        # Розрахунок загальної ширини і висоти дошки
        self.board_width = self.square_size * self.cols
        self.board_height = self.square_size * (self.rows + 1)

        # Розрахунок відступів для центрування
        self.offset_x = (self.screen_width - self.board_width) // 2
        self.offset_y = (self.screen_height - self.board_height) // 2

        # Розрахунок радіуса фішок
        self.radius = int(self.square_size * 0.4)

    def get_column_from_pos(self, pos_x):
        """Повертає номер колонки для заданої позиції x."""
        if pos_x < self.offset_x or pos_x >= self.offset_x + self.board_width:
            return None
        return (pos_x - self.offset_x) // self.square_size

    def draw_hover_piece(self):
        """Малює фішку, що зависає над дошкою."""
        if self.hover_col is not None and not self.is_animating:
            color = self.red if self.current_player == 1 else self.yellow
            center_x = self.offset_x + self.hover_col * self.square_size + self.square_size // 2
            pygame.draw.circle(self.screen, color,
                               (center_x, self.offset_y + self.square_size // 2),
                               self.radius)

    def draw_hover(self, pos_x):
        """Оновлює позицію фішки, що зависає."""
        self.hover_col = self.get_column_from_pos(pos_x)
        self.draw_board()

    def is_winner(self, player):
        """Перевіряє, чи гравець виграв гру."""
        # Перевірка по горизонталі, вертикалі та діагоналях
        for r in range(self.rows):
            for c in range(self.cols - 3):
                if all(self.board[r][c + i] == player for i in range(4)):
                    return True
        for r in range(self.rows - 3):
            for c in range(self.cols):
                if all(self.board[r + i][c] == player for i in range(4)):
                    return True
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                if all(self.board[r + i][c + i] == player for i in range(4)):
                    return True
                if all(self.board[r + 3 - i][c + i] == player for i in range(4)):
                    return True
        return False

    def is_draw(self):
        """Перевіряє, чи поле заповнене і немає переможця."""
        return all(self.board[0][c] != 0 for c in range(self.cols))

    def reset(self):
        """Скидає ігрову дошку."""
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_player = 1