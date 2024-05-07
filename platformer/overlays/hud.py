# Standard Library Imports


# Third-Party Imports
import pygame

# Local Imports
import settings


class HUD:

    def __init__(self, game):
        self.game = game

        self.primary_font = pygame.font.Font(settings.PRIMARY_FONT, 32)
        self.secondary_font = pygame.font.Font(settings.SECONDARY_FONT, 16)
        
    def update(self):
        pass

    def draw(self, surface):
        text = self.primary_font.render(f"Level: {self.game.level}", True, settings.WHITE)
        rect = text.get_rect()
        rect.topleft = 16, 16
        surface.blit(text, rect)

        text = self.primary_font.render(f"Score: {self.game.hero.score}", True, settings.WHITE)
        rect = text.get_rect()
        rect.topleft = 16, 56
        surface.blit(text, rect)

        text = self.primary_font.render(f"Hearts: {self.game.hero.hearts}", True, settings.WHITE)
        rect = text.get_rect()
        rect.topleft = 16, 96
        surface.blit(text, rect)
