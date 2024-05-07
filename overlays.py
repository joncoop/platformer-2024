import pygame

import settings


class TitleScreen:

    def __init__(self, game):
        self.game = game

        self.title_font = pygame.font.Font(settings.PRIMARY_FONT, 80)
        self.subtitle_font = pygame.font.Font(settings.SECONDARY_FONT, 32)
        
    def update(self):
        pass

    def draw(self, surface):
        text = self.title_font.render(settings.TITLE, True, settings.WHITE)
        rect = text.get_rect()
        rect.centerx = settings.SCREEN_WIDTH // 2
        rect.bottom = settings.SCREEN_HEIGHT // 2 - 8
        surface.blit(text, rect)
    
        text = self.subtitle_font.render("Press 'SPACE' to start.", True, settings.WHITE)
        rect = text.get_rect()
        rect.centerx = settings.SCREEN_WIDTH // 2
        rect.top = settings.SCREEN_HEIGHT // 2 + 8
        surface.blit(text, rect)


class WinScreen:

    def __init__(self, game):
        self.game = game

        self.title_font = pygame.font.Font(settings.PRIMARY_FONT, 80)
        self.subtitle_font = pygame.font.Font(settings.SECONDARY_FONT, 32)
        
    def update(self):
        pass

    def draw(self, surface):
        text = self.title_font.render("You win!", True, settings.WHITE)
        rect = text.get_rect()
        rect.centerx = settings.SCREEN_WIDTH // 2
        rect.bottom = settings.SCREEN_HEIGHT // 2 - 8
        surface.blit(text, rect)
    
        text = self.subtitle_font.render("Press 'r' to play again.", True, settings.WHITE)
        rect = text.get_rect()
        rect.centerx = settings.SCREEN_WIDTH // 2
        rect.top = settings.SCREEN_HEIGHT // 2 + 8
        surface.blit(text, rect)


class LoseScreen:

    def __init__(self, game):
        self.game = game

        self.title_font = pygame.font.Font(settings.PRIMARY_FONT, 80)
        self.subtitle_font = pygame.font.Font(settings.SECONDARY_FONT, 32)
        
    def update(self):
        pass

    def draw(self, surface):
        text = self.title_font.render("You lose!", True, settings.WHITE)
        rect = text.get_rect()
        rect.centerx = settings.SCREEN_WIDTH // 2
        rect.bottom = settings.SCREEN_HEIGHT // 2 - 8
        surface.blit(text, rect)
    
        text = self.subtitle_font.render("Press 'r' to play again.", True, settings.WHITE)
        rect = text.get_rect()
        rect.centerx = settings.SCREEN_WIDTH // 2
        rect.top = settings.SCREEN_HEIGHT // 2 + 8
        surface.blit(text, rect)


class LevelCompleteScreen:

    def __init__(self, game):
        self.game = game

        self.title_font = pygame.font.Font(settings.SECONDARY_FONT, 32)
        
    def update(self):
        pass

    def draw(self, surface):
        text = self.title_font.render("Level Complete!", True, settings.WHITE)
        rect = text.get_rect()
        rect.centerx = settings.SCREEN_WIDTH // 2
        rect.bottom = settings.SCREEN_HEIGHT // 2 - 8
        surface.blit(text, rect)


class PauseScreen:

    def __init__(self, game):
        self.game = game

        self.title_font = pygame.font.Font(settings.PRIMARY_FONT, 80)
        self.subtitle_font = pygame.font.Font(settings.SECONDARY_FONT, 32)
        
    def update(self):
        pass

    def draw(self, surface):
        text = self.subtitle_font.render("Paused", True, settings.WHITE)
        rect = text.get_rect()
        rect.centerx = settings.SCREEN_WIDTH // 2
        rect.bottom = settings.SCREEN_HEIGHT // 2 - 8
        surface.blit(text, rect)
    
        text = self.subtitle_font.render("Press 'p' to continue", True, settings.WHITE)
        rect = text.get_rect()
        rect.centerx = settings.SCREEN_WIDTH // 2
        rect.top = settings.SCREEN_HEIGHT // 2 + 8
        surface.blit(text, rect)


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



# Used for level editing
class Grid:

    def __init__(self, game, color=(125, 125, 125)):
        self.game = game
        self.on = False

        self.color = color
        self.font = pygame.font.Font(None, 16)

    def toggle(self):
        self.on = not self.on

    def draw(self, surface, offset_x=0, offset_y=0):
        if self.on:
            width = surface.get_width()
            height = surface.get_height()
            
            for x in range(0, width + settings.GRID_SIZE, settings.GRID_SIZE):
                adj_x = x - offset_x % settings.GRID_SIZE
                pygame.draw.line(surface, self.color, [adj_x, 0], [adj_x, height], 1)

            for y in range(0, height + settings.GRID_SIZE, settings.GRID_SIZE):
                adj_y = y - offset_y % settings.GRID_SIZE
                pygame.draw.line(surface, self.color, [0, adj_y], [width, adj_y], 1)

            for x in range(0, width + settings.GRID_SIZE, settings.GRID_SIZE):
                for y in range(0, height + settings.GRID_SIZE, settings.GRID_SIZE):
                    adj_x = x - offset_x % settings.GRID_SIZE + 4
                    adj_y = y - offset_y % settings.GRID_SIZE + 4
                    disp_x = x // settings.GRID_SIZE + offset_x // settings.GRID_SIZE
                    disp_y = y // settings.GRID_SIZE + offset_y // settings.GRID_SIZE
                    
                    point = f'({disp_x}, {disp_y})'
                    text = self.font.render(point, True, self.color)
                    surface.blit(text, [adj_x, adj_y])
