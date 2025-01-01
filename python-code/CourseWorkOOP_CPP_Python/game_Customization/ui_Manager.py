import pygame
import sys

class VictoryScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 50)
        self.showing = False
        self.start_time = 0

    def draw(self, winner):
        if not self.showing:
            self.showing = True
            self.start_time = pygame.time.get_ticks()

        text = "Нічия!" if winner == "draw" else f"{winner} переміг!"
        text_surface = self.font.render(text, True, (255, 255, 255))

        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 0, 0, 128), overlay.get_rect())

        glow_surfaces = []
        for i in range(3):
            size = 50 + i * 2
            glow_font = pygame.font.SysFont("arial", size)
            glow_surface = glow_font.render(text, True, (255, 255, 255))
            glow_surface.set_alpha(50 - i * 15)
            glow_surfaces.append(glow_surface)

        self.screen.blit(overlay, (0, 0))

        screen_width, screen_height = self.screen.get_size()
        for glow_surface in glow_surfaces:
            x = (screen_width - glow_surface.get_width()) // 2
            y = (screen_height - glow_surface.get_height()) // 2
            self.screen.blit(glow_surface, (x, y))

        x = (screen_width - text_surface.get_width()) // 2
        y = (screen_height - text_surface.get_height()) // 2
        self.screen.blit(text_surface, (x, y))
        pygame.display.update()

        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= 3000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            return True
        return False