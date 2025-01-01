import pygame
from Menu.state_Manager import StateManager

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Connect four")
    state_manager = StateManager(screen)
    state_manager.run()
