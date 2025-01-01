from Game.Connect_Four_Game import ConnectFourGame
from game_Customization.ui_Manager import VictoryScreen
from Bot.Bot import ConnectFourAI, Difficulty
import pygame
import sys

class GameWithAI(ConnectFourGame):
    def __init__(self, screen, rows=6, cols=7, difficulty="medium"):
        super().__init__(screen, rows, cols)
        self.ai_thinking = False
        self.ai_move_col = None
        self.ai_timer = 0
        self.ai_delay = 1000
        self.clock = pygame.time.Clock()
        self.winner = None
        self.victory_screen = VictoryScreen(self.screen)

        # Ініціалізація C++ AI
        self.ai = ConnectFourAI(rows, cols)

        self.difficulty_map = {
            "easy": Difficulty.EASY,
            "medium": Difficulty.MEDIUM,
            "hard": Difficulty.HARD
        }

        # Встановлення початкового рівня складності
        if difficulty and isinstance(difficulty, str):
            self.set_difficulty(difficulty)
        else:
            self.difficulty = None

    def set_difficulty(self, difficulty):
        """Встановлення рівня складності з UI"""
        if not difficulty:
            return False

        difficulty = str(difficulty).lower()
        if difficulty in self.difficulty_map:
            self.difficulty = difficulty
            return True
        return False

    def can_start_game(self):
        """Перевірка чи можна розпочати гру"""
        return self.difficulty is not None

    def handle_player_move(self, x):
        """Обробка ходу гравця"""
        if not self.can_start_game():
            return False

        col = self.get_column_from_pos(x)
        if col is not None and self.board[0][col] == 0:
            self.make_move(col)
            if self.check_game_over():
                return True
        return False

    def make_move(self, col):
        """Виконання ходу"""
        if self.drop_piece(col):
            if self.is_winner(self.current_player):
                self.winner = "Гравець" if self.current_player == 1 else "AI"
                return True
            elif self.is_draw():
                self.winner = "draw"
                return True
            self.switch_player()
            return False
        return False

    def handle_ai_move(self, current_time):
        """Обробка ходу AI"""
        if not self.can_start_game():
            return False

        if not self.is_animating and not self.ai_thinking:
            if current_time - self.ai_timer >= self.ai_delay:
                self.ai_thinking = True
                self.ai_move_col = self.get_ai_move()

                if self.ai_move_col is not None:
                    if self.make_move(self.ai_move_col):
                        return True

                self.ai_thinking = False
        return False

    def get_ai_move(self):
        """Отримання ходу від AI"""
        if not self.can_start_game():
            return None

        difficulty = self.difficulty_map[self.difficulty]
        return self.ai.get_move(self.board, difficulty)

    def check_game_over(self):
        """Перевірка закінчення гри"""
        if self.is_winner(self.current_player):
            self.winner = "Гравець" if self.current_player == 1 else "AI"
            return True
        elif self.is_draw():
            self.winner = "draw"
            return True
        return False

    def handle_animation(self):
        """Обробка анімації падіння фішки"""
        if self.is_animating:
            if self.update_animation():
                return self.check_game_over()
        return False

    def play(self):
        """Головний цикл гри"""
        if not self.can_start_game():
            print("Cannot start game without selecting difficulty")
            return

        running = True
        while running:
            self.draw_board()
            current_time = pygame.time.get_ticks()

            # Обробка подій
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.current_player == 1:  # Хід гравця
                    if event.type == pygame.MOUSEMOTION:
                        self.draw_hover(event.pos[0])
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.handle_player_move(event.pos[0]):
                            running = False
                        else:
                            self.ai_timer = current_time

            # Хід AI
            if self.current_player == 2:
                if self.handle_ai_move(current_time):
                    running = False

            # Оновлення анімації
            if self.handle_animation():
                running = False

            pygame.display.flip()
            self.clock.tick(60)

        # Показ фінального стану гри
        self.draw_board()

        # Екран перемоги
        while True:
            if self.victory_screen.draw(self.winner):
                break

    def __del__(self):
        """Очищення ресурсів при знищенні об'єкта"""
        if hasattr(self, 'ai'):
            del self.ai