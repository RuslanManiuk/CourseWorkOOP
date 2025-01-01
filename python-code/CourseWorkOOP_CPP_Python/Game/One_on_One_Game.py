import pygame
import sys
from Game.Connect_Four_Game import ConnectFourGame
from game_Customization.ui_Manager import VictoryScreen

class OneOnOneGame(ConnectFourGame):
    def __init__(self, screen, rows, cols):
        super().__init__(screen, rows, cols)
        self.screen = screen
        self.cell_size = 80  # Розмір клітинки
        self.offset = 50  # Зсув від краю екрану
        self.font = pygame.font.SysFont("arial", 50)
        self.clock = pygame.time.Clock()

        self.victory_screen = VictoryScreen(self.screen)

    def play(self):
        self.draw_board()
        game_over = False

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.screen = screen
                    self.recalculate_dimensions()
                    self.draw_board()

                if event.type == pygame.MOUSEMOTION:
                    self.hover_col = self.get_column_from_pos(event.pos[0])
                    self.draw_board()

                if event.type == pygame.MOUSEBUTTONDOWN and not self.is_animating:
                    col = self.get_column_from_pos(event.pos[0])
                    self.drop_piece(col)

            # Оновлення анімації
            if self.is_animating:
                if self.update_animation():
                    if self.is_winner(self.current_player):
                        self.winner = "Гравець 1" if self.current_player == 1 else "Гравець 2"
                        self.victory_screen.draw(self.winner)
                        game_over = True
                    elif self.is_draw():
                        self.victory_screen.draw("draw")
                        game_over = True
                    else:
                        self.switch_player()

            self.draw_board()
            self.clock.tick(60)

            if game_over:
                self.victory_screen.draw(self.winner)
                while True:
                    if self.victory_screen.draw(self.winner):
                        break
                pygame.time.wait(3000)